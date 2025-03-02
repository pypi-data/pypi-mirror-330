import asyncio
from dataclasses import dataclass

from google.genai import types
from google.genai.errors import ClientError
from rich.progress import Progress

from .intelligence.client import audio_to_subtitles, upload_file, delete_file, RateLimitExceededError
from .media.info import get_duration
from .subtitles.serializer import serialize_subtitles
from .subtitles.validator import validate_subtitles, SubtitleValidationError
from .system.directory import paths_with_offsets
from .system.language import get_language_name
from .system.logger import write_log
from .system.rate_limiter import RateLimiter
from .system.console import info, error, log, status


rate_limiter = RateLimiter(rate_limit=10, period=60)


@dataclass
class TranscribeConfig:
    directory: str = "tmp"


def transcribe(parsed, config: TranscribeConfig = TranscribeConfig()) -> None:
    asyncio.run(_transcribe(parsed, config))


async def _transcribe(parsed, config: TranscribeConfig) -> None:
    with status("Uploading files..."):
        tasks = []

        path_offset_list = paths_with_offsets(parsed.audio_segment_prefix, parsed.audio_segment_format, f"./{config.directory}")
        for path, offset in path_offset_list:
            async def run(path, offset):
                file_path = f"{config.directory}/{path}"
                file = await upload_file(parsed.gemini_api_key, file_path)
                duration_ms = get_duration(file_path) * 1000
                return (offset, file, duration_ms)
            task = asyncio.create_task(run(path, offset))
            tasks.append(task)

        results = await asyncio.gather(*tasks)
        offset_file_duration_dict = {offset: (file, duration_ms) for offset, file, duration_ms in results}
        offset_file_duration_list = sorted(offset_file_duration_dict.items(), key=lambda item: int(item[0]))

    info("Transcribing files...")
    tasks = []

    with Progress() as progress:
        for language_code in parsed.languages:
            language_name = get_language_name(language_code)
            progress_task = progress.add_task(language_name, total=len(offset_file_duration_list))

            for offset, (file, duration_ms) in offset_file_duration_list:
                async def run(file, duration_ms, offset, language_code, progress_task):
                    await _transcribe_item(
                        file,
                        int(duration_ms),
                        parsed.audio_segment_format,
                        offset,
                        language_code,
                        parsed.gemini_api_key,
                        parsed.retry,
                        parsed.debug,
                        config,
                    )
                    progress.update(progress_task, advance=1)
                task = asyncio.create_task(run(file, duration_ms, offset, language_code, progress_task))
                tasks.append(task)

        await asyncio.gather(*tasks)

    for _, (file, _) in offset_file_duration_list:
        try:
            await delete_file(parsed.gemini_api_key, file)
        except Exception as e:
            error(f"Failed to delete file: {str(e)}")


async def _transcribe_item(
    file: types.File,
    duration_ms: int,
    audio_segment_format: str,
    offset: int,
    language_code: str,
    api_key: str,
    retry: int,
    debug: bool,
    config: TranscribeConfig,
) -> None:
    language = get_language_name(language_code)

    try:
        for attempt in range(retry):
            # Apply rate limiting for the audio_to_subtitles call
            await rate_limiter.acquire()

            try:
                subtitles = await audio_to_subtitles(api_key, file, audio_segment_format, language)

                try:
                    validate_subtitles(subtitles, duration_ms)

                    if debug:
                        write_log(f"{language_code}_{offset}", "Valid", language, offset, subtitles, directory=f"./{config.directory}")
                    serialize_subtitles(subtitles, language_code, int(offset), config.directory)
                    break  # Happy path

                except SubtitleValidationError as e:
                    if debug:
                        write_log(f"{language_code}_{offset}", "Invalid", e, language, offset, subtitles, directory=f"./{config.directory}")

                    # Use consistent backoff strategy
                    wait_time = min(2**attempt, 60)
                    await asyncio.sleep(wait_time)

            except RateLimitExceededError:
                if debug:
                    write_log(f"{language_code}_{offset}", "Rate Limit Exceeded", "API rate limit exceeded", language, offset, directory=f"./{config.directory}")
            except ClientError as e:
                if debug:
                    write_log(f"{language_code}_{offset}", "API Error", f"ClientError: {e}", language, offset, directory=f"./{config.directory}")
            except Exception as e:
                if debug:
                    write_log(f"{language_code}_{offset}", "Unexpected Error", f"Exception: {e}", language, offset, directory=f"./{config.directory}")

            # Use consistent backoff strategy
            wait_time = min(2**attempt, 60)
            await asyncio.sleep(wait_time)

    except Exception as e:
        if debug:
            error(f"Error in transcription process: {str(e)}")
