from dataclasses import dataclass
from enum import Enum, auto
from typing import Generic, TypedDict, TypeVar

from sh import Command
from typer import Context


class RawReviewRequest(TypedDict):
    """User that was asked to review a PR."""

    login: str
    name: str


class RawStatusCheck(TypedDict):
    """PR Status Check."""

    conclusion: str


class RawPullRequest(TypedDict):
    """Description of a PR from GitHub CLI."""

    number: int
    baseRefName: str
    headRefName: str
    title: str
    url: str
    id: str
    isDraft: bool
    mergeable: str
    reviewDecision: str
    reviewRequests: list[RawReviewRequest]
    statusCheckRollup: list[RawStatusCheck]


class PullRequestStatus(TypedDict):
    """Raw output from gh CLI."""

    createdBy: list[RawPullRequest]
    currentBranch: RawPullRequest


class ChecksStatus(Enum):
    """Status of PR checks."""

    SUCCESS = auto()
    FAILURE = auto()
    RUNNING = auto()


@dataclass
class PullRequest:
    """Describe a GitHub PR."""

    number: int
    branch: str
    base_branch: str
    title: str
    url: str
    is_current: bool
    review_decision: str
    mergeable: str
    is_draft: bool
    reviewers: list[str]
    checks_status: ChecksStatus

    def __repr__(self):
        """Represent a PR for printing."""
        return (
            f'#{self.number} {self.title} | '
            f'{self.branch} → {self.base_branch}'  # noqa: WPS326
        )


@dataclass
class State:
    """Application state."""

    current_branch: str
    stack: list[PullRequest]
    gh: Command
    current_pull_request: PullRequest | None = None


StateType = TypeVar('StateType')


class TypedContext(Context, Generic[StateType]):
    """Typed context."""

    obj: StateType   # noqa: WPS110


class PRStackContext(TypedContext[State]):
    """Typed context for Jeeves PR Stack app."""


@dataclass
class Commit:
    """Git commit."""

    oid: str
    title: str
