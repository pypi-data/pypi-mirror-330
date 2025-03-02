from __future__ import annotations
import dataclasses
import enum
import re


class OutputFormat(enum.Enum):
    none = enum.auto()
    srt = enum.auto()
    diffable_srt = enum.auto()


class SRT:
    # Can't use the one from Timecode because that has named groups, which can't be duplicates
    timecode_pattern_str = r"\d\d:\d\d:\d\d,\d\d\d"
    timing_line_pattern = re.compile(
        rf"({timecode_pattern_str}) --> ({timecode_pattern_str})"
    )

    def __init__(self):
        self.events: list[Event] = []

    @staticmethod
    def from_str(text: str) -> SRT:

        srt = SRT()
        counter = 1
        events = [event for event in text.split("\n\n") if event.strip()]
        for event_str in events:
            lines = event_str.split("\n")
            counter_str, timing_str, content_lines = lines[0], lines[1], lines[2:]

            if int(counter_str) != counter:
                raise ParseError(
                    f"Invalid counter '{counter_str}'; expected {counter}", event_str
                )
            counter += 1

            match = re.fullmatch(SRT.timing_line_pattern, timing_str)
            if match is None:
                raise ParseError(f"Invalid timing info '{timing_str}'", event_str)

            content = "\n".join(content_lines + [""])

            srt.events.append(Event(Timecode(match[1]), Timecode(match[2]), content))

        return srt

    def __str__(self):
        return self.to_output_format(OutputFormat.srt)

    def to_output_format(self, format: OutputFormat) -> str:
        result = ""
        match format:
            case OutputFormat.none:
                pass
            case OutputFormat.srt:
                for counter, event in enumerate(self.events, 1):
                    result += f"{counter}\n"
                    result += f"{event.start} --> {event.end}\n"
                    result += f"{event.content}\n"
            case OutputFormat.diffable_srt:
                # Not an actual subtitle format, just drops the counter to
                # make it easier to diff actual changes (in timing/content).
                for event in self.events:
                    result += f"{event.start} --> {event.end}\n"
                    result += f"{event.content}\n"
        return result


@dataclasses.dataclass
class Event:
    start: Timecode
    end: Timecode
    content: str


class Timecode:
    timecode_pattern = re.compile(
        r"(?P<hour>\d\d):(?P<minute>\d\d):(?P<second>\d\d),(?P<millisecond>\d\d\d)"
    )

    def __init__(self, timecode_str: str):
        match = re.fullmatch(self.timecode_pattern, timecode_str)
        if match is None:
            raise ParseError(f"Invalid timecode '{timecode_str}'", timecode_str)
        self.hour = int(match["hour"])
        self.minute = int(match["minute"])
        self.second = int(match["second"])
        self.millisecond = int(match["millisecond"])

    def __repr__(self):
        return f"Timecode('{str(self)}')"

    def __str__(self):
        return f"{self.hour:02}:{self.minute:02}:{self.second:02},{self.millisecond:03}"


class ParseError(Exception):
    def __init__(self, reason: str, context_str: str):
        super().__init__(f"{reason}\nwhile parsing the following:\n{context_str}")
        self.reason = reason
        self.event_str = context_str
