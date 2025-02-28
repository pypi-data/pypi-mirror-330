try:
    import logging
    import sys
    from pathlib import Path

    from s4f.compile_command import compile_protos

    logger = logging.getLogger("s4f.compile_command")
    if not logger.hasHandlers():
        logger.addHandler(logging.StreamHandler(sys.stdout))
        logger.info("Compiling protos for sponsored-ads-service.")

    compile_protos(Path(__file__).parent)
except ImportError:
    print(  # noqa: T201
        "Could not import compile_protos from s4f.compile_command. Skipping compilation of protos."
    )
