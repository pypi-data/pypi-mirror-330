import coloredlogs


def setup_standard_log():
    coloredlogs.install(
        fmt="(%(relativeCreated)6d) [%(levelname)s] %(name)s: %(message)s",
        level="INFO",
        field_styles=dict(
            relativeCreated={"color": "black"},
            levelname={"color": "white", "bold": True},
            name={"color": "blue"},
        ),
    )
