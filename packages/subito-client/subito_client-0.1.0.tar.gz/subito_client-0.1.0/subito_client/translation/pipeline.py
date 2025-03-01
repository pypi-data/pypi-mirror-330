import aiohttp
import os
from pathlib import Path
from typing import Optional, List, Dict

from ..configs import SERVER_CONF, RETRY_CONF, PREFIX, ServerConfig, RetryConfig
from .operations import (
    prepare_files,
    upload_file,
    start_translation,
    wait_for_translation,
    retry_download,
    process_translated_file,
    TranslationContext
)


async def translate_folder(
    folder_path: str,
    token: str,
    max_price: int = None,
    server_config: ServerConfig = SERVER_CONF,
    retry_config: RetryConfig = RETRY_CONF,
    prefix: str = PREFIX
) -> Dict[str, List[Path]]:
    """
    Translate all files in a folder, processing them one by one.
    
    Returns a dictionary with 'successful' and 'failed' lists of file paths.
    """
    folder = Path(folder_path)
    
    if not folder.exists() or not folder.is_dir():
        raise ValueError(f"Folder path {folder_path} does not exist or is not a directory")
    
    results = {
        'successful': [],
        'failed': []
    }
    
    # Get all files in the folder (non-recursive)
    files = [f for f in folder.iterdir() if f.is_file()]
    
    if not files:
        print(f"No files found in {folder_path}")
        return results
    
    # Process each file one by one
    for file_path in files:
        print(f"Processing file: {file_path.name}")
        translated_path = await translate_file(
            str(file_path),
            token,
            max_price,
            server_config,
            retry_config,
            prefix
        )
        
        if translated_path:
            results['successful'].append(translated_path)
            print(f"Successfully translated: {file_path.name}")
        else:
            results['failed'].append(file_path)
            print(f"Failed to translate: {file_path.name}")
    
    # Print summary
    print(f"\nTranslation complete:")
    print(f"- Successfully translated: {len(results['successful'])} files")
    print(f"- Failed to translate: {len(results['failed'])} files")
    
    return results


async def translate_file(
    file_path: str,
    token: str,
    max_price: int = None,
    server_config: ServerConfig = SERVER_CONF,
    retry_config: RetryConfig = RETRY_CONF,
    prefix: str = PREFIX
) -> Path | None:
    """Upload a file for translation, wait for completion, and return the path to the translated file"""
    async with aiohttp.ClientSession() as session:
        # Prepare context with necessary file information
        ctx = await _prepare_translation_context(file_path)
        if not ctx:
            return None
            
        # Handle the main translation workflow
        try:
            await _upload_and_check_price(session, ctx, token, server_config, max_price)
            if not ctx.file_id:  # Upload failed or price exceeded maximum
                return None
                
            await _process_translation(session, ctx, token, server_config, retry_config, prefix)
            if not ctx.downloaded_path:  # Translation or download failed
                return None
                
            # Process the final translated file
            process_translated_file(ctx, prefix)
            return ctx.output_path
            
        except Exception as e:
            print(f"Translation error: {str(e)}")
            _cleanup_temp_files(ctx)
            return None


async def _prepare_translation_context(file_path: str) -> Optional[TranslationContext]:
    """Prepare the translation context with file information"""
    try:
        return prepare_files(file_path)
    except Exception as e:
        print(f"Error preparing files: {e}")
        return None


async def _upload_and_check_price(
    session: aiohttp.ClientSession,
    ctx: TranslationContext,
    token: str,
    server_config: ServerConfig,
    max_price: Optional[int]
) -> None:
    """Upload the file and check if price is within acceptable range"""
    try:
        upload_response = await upload_file(session, ctx.upload_path, token, server_config)
        ctx.file_id = upload_response.file_id
        ctx.price = upload_response.price
        
        # Check price limits
        if (max_price is not None) and (ctx.price > max_price):
            print(f"Price {ctx.price} exceeds maximum allowed {max_price}. Aborting.")
            _cleanup_temp_files(ctx)
            ctx.file_id = None  # Mark as failed
    except Exception as e:
        _cleanup_temp_files(ctx)
        raise e


async def _process_translation(
    session: aiohttp.ClientSession,
    ctx: TranslationContext,
    token: str,
    server_config: ServerConfig,
    retry_config: RetryConfig,
    prefix: str
) -> None:
    """Start translation, wait for completion, and handle download"""
    # Start translation process
    await start_translation(session, ctx.file_id, token, server_config)

    # Wait for translation to complete
    translation_completed = await wait_for_translation(
        session, ctx, token, server_config, retry_config, prefix
    )
    
    # Final download attempt if needed
    if not translation_completed or ctx.downloaded_path is None:
        print("Translation status uncertain or download not confirmed. Making final download attempts...")
        ctx.downloaded_path = await retry_download(
            session=session,
            file_id=ctx.file_id,
            token=token,
            original_path=ctx.upload_path,
            prefix=prefix,
            server_config=server_config
        )


def _cleanup_temp_files(ctx: TranslationContext) -> None:
    """Clean up any temporary files created during the process"""
    if ctx.temp_srt_path:
        ctx.temp_srt_path.unlink(missing_ok=True)


async def translate(
    path: str,
    token: str = "",
    max_price: int = None,
    server_config: ServerConfig = SERVER_CONF,
    retry_config: RetryConfig = RETRY_CONF,
    prefix: str = PREFIX
) -> Path | Dict[str, List[Path]]:
    """
    Translates a single file or all files in a directory.
    
    Args:
        path: Path to a file or directory to translate
        token: Authentication token (if None, will try to use SUBITO_TOKEN environment variable)
        max_price: Maximum price allowed for translation
        server_config: Server configuration
        retry_config: Retry configuration
        prefix: Prefix for translated files
        
    Returns:
        For a file: Path to the translated file or None if failed
        For a directory: Dictionary with 'successful' and 'failed' lists of file paths
    """
    # Get token from environment variable if not provided
    if token == "":
        env_token = os.environ.get("SUBITO_TOKEN", None)
        print(f"Reading from environment: SUBITO_TOKEN = {env_token}")
        token = env_token
        del env_token
    
        if token == "":
            raise ValueError("Translation token is required. Provide it as a parameter or set SUBITO_TOKEN environment variable.")
    
    input_path = Path(path)
    
    # Check if path exists
    if not input_path.exists():
        raise ValueError(f"Path {path} does not exist")
    
    # Determine if it's a file or folder and call appropriate function
    if input_path.is_file():
        print(f"Processing single file: {input_path.name}")
        return await translate_file(
            str(input_path),
            token,
            max_price,
            server_config,
            retry_config,
            prefix
        )
    elif input_path.is_dir():
        print(f"Processing folder: {input_path}")
        return await translate_folder(
            str(input_path),
            token,
            max_price,
            server_config,
            retry_config,
            prefix
        )
    else:
        raise ValueError(f"Path {path} is neither a file nor a directory") 