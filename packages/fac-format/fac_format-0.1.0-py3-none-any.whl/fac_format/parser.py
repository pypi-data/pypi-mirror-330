"""
FAC Format Parser and Writer
A deliberately complicated and inefficient file format alternative to JSON
"""

class FacParser:
    def __init__(self):
        self.current_line = 0
        self.lines = []

    def parse(self, content):
        """Parse a .fac file content into Python objects"""
        self.lines = content.split('\n')
        self.current_line = 0

        if not self._validate_header():
            raise ValueError("Invalid FAC file: Missing or invalid header")

        return self._parse_block()

    def _validate_header(self):
        """Check if file starts with required header"""
        if self.current_line >= len(self.lines):
            return False
        line = self.lines[self.current_line].strip()
        self.current_line += 1
        return line == "@begin/format@"

    def _parse_block(self):
        """Parse a block of FAC content"""
        result = {}

        while self.current_line < len(self.lines):
            line = self.lines[self.current_line].strip()

            if line == "@end/format@":
                self.current_line += 1
                return result

            if not line or line.startswith('\\note'):
                self.current_line += 1
                continue

            # Parse key-value pairs
            if line.startswith('@value|'):
                key, value = self._parse_value()
                result[key] = value

            # Parse lists
            elif line.startswith('@list|'):
                key, value = self._parse_list()
                result[key] = value

            # Parse nested objects
            elif line.startswith('@object|'):
                key, value = self._parse_object()
                result[key] = value

            self.current_line += 1

        raise ValueError("Invalid FAC file: Missing end marker")

    def _parse_value(self):
        """Parse a simple value declaration"""
        line = self.lines[self.current_line]
        parts = line.split('@value|')
        if len(parts) != 2:
            raise ValueError(f"Invalid value declaration at line {self.current_line + 1}")

        key = parts[1].strip()

        self.current_line += 1
        if self.current_line >= len(self.lines):
            raise ValueError(f"Missing value for key {key}")

        value_line = self.lines[self.current_line].strip()
        if not value_line.startswith('/content\\'):
            raise ValueError(f"Invalid value format at line {self.current_line + 1}")

        value = value_line.replace('/content\\', '').strip()

        # Parse different value types
        if value.startswith('|number|'):
            return key, float(value.replace('|number|', '').strip())
        elif value.startswith('|text|'):
            return key, value.replace('|text|', '').strip()
        elif value.startswith('|boolean|'):
            return key, value.replace('|boolean|', '').strip() == 'true'
        else:
            return key, value

    def _parse_list(self):
        """Parse a list declaration"""
        line = self.lines[self.current_line]
        parts = line.split('@list|')
        key = parts[1].strip()

        values = []
        self.current_line += 1

        while self.current_line < len(self.lines):
            line = self.lines[self.current_line].strip()

            if line == '/end\\list':
                return key, values

            if line.startswith('|item\\'):
                value = line.replace('|item\\', '').strip()
                values.append(value)

            self.current_line += 1

        raise ValueError("Invalid FAC file: Missing end list marker")

    def _parse_object(self):
        """Parse a nested object declaration"""
        line = self.lines[self.current_line]
        parts = line.split('@object|')
        key = parts[1].strip()

        self.current_line += 1
        nested_result = {}

        while self.current_line < len(self.lines):
            line = self.lines[self.current_line].strip()

            if line == '/end\\object':
                return key, nested_result

            if line.startswith('@value|'):
                nested_key, value = self._parse_value()
                nested_result[nested_key] = value
            elif line.startswith('@list|'):
                nested_key, value = self._parse_list()
                nested_result[nested_key] = value

            self.current_line += 1

        raise ValueError("Invalid FAC file: Missing end object marker")

class FacWriter:
    @staticmethod
    def write(data):
        """Convert Python objects to FAC format"""
        output = ["@begin/format@"]

        for key, value in data.items():
            output.extend(FacWriter._write_value(key, value))

        output.append("@end/format@")
        return "\n".join(output)

    @staticmethod
    def _write_value(key, value):
        """Convert a single value to FAC format"""
        if isinstance(value, (list, tuple)):
            return FacWriter._write_list(key, value)
        elif isinstance(value, dict):
            return FacWriter._write_object(key, value)
        else:
            return FacWriter._write_simple_value(key, value)

    @staticmethod
    def _write_simple_value(key, value):
        """Convert a simple value to FAC format"""
        if isinstance(value, bool):
            return [
                f"@value|{key}",
                f"/content\\|boolean|{'true' if value else 'false'}"
            ]
        elif isinstance(value, (int, float)):
            return [
                f"@value|{key}",
                f"/content\\|number|{value}"
            ]
        else:
            return [
                f"@value|{key}",
                f"/content\\|text|{value}"
            ]

    @staticmethod
    def _write_list(key, values):
        """Convert a list to FAC format"""
        output = [f"@list|{key}"]
        for value in values:
            output.append(f"|item\\{value}")
        output.append("/end\\list")
        return output

    @staticmethod
    def _write_object(key, value):
        """Convert a nested object to FAC format"""
        output = [f"@object|{key}"]
        for k, v in value.items():
            output.extend(FacWriter._write_value(k, v))
        output.append("/end\\object")
        return output