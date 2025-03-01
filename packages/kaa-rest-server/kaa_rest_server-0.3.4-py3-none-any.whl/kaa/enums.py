from enum import Enum


class Status(Enum):
    OK = [200, "200 Ok"]
    CREATED = [201, "201 Created"]
    ACCEPTED = [202, "202 Accepted"]
    NO_CONTENT = [204, "204 No content"]
    MOVED_PERMANENTLY = [301, "301 Moved permanently"]
    FOUND = [302, "302 Found"]
    BAD_REQUEST = [400, "400 Bad request"]
    UNAUTHORIZED = [401, "401 Unauthorized"]
    FORBIDDEN = [403, "403 Forbidden"]
    NOT_FOUND = [404, "404 Not found"]
    METHOD_NOT_ALLOWED = [405, "405 Method not allowed"]
    SERVER_ERROR = [500, "500 Server error"]


class ContentType(Enum):
    PLAIN = "text/plain"
    HTML = "text/html"
    JSON = "application/json"
    YAML = "application/x-yaml"
