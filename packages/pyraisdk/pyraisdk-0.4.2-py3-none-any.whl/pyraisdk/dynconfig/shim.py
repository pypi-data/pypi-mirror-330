
# Since AML infra depends on pydantic v1, and pyraisdk is always used with AML
# infra most of the time. So we have to use pydantic v1 inside pyraisdk. 
# But in order to avoid that other projects using pyraisdk can't use pydantic v2,
# we want to have compatibility between the two versions of pydantic within pyraisdk.


from typing import TYPE_CHECKING
from packaging import version
import pydantic


if TYPE_CHECKING:
    # You need to cheat the type checker in this way. Otherwise, even if
    # it works, the type checker will report errors.
    import pydantic.v1 as pydantic_v1
else:
    if version.parse(pydantic.__version__).major > 1:
        import pydantic.v1 as pydantic_v1
    else:
        import pydantic as pydantic_v1
