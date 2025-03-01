"""Base classes for rules and rule sets."""

from abc import ABC, abstractmethod, ABCMeta
from collections.abc import Iterator
from dataclasses import dataclass
from enum import Enum
from typing import TypeVar
from typing import Union, Generic

from pydantic import BaseModel, ConfigDict

from lintr.rules.context import RuleContext
from lintr.util import camel_to_hyphen


class RuleCategoryValue(BaseModel):
    """Value for a rule category."""

    name: str
    code: str
    description: str


class RuleCategory(Enum):
    """Categories for rules."""

    GENERAL = RuleCategoryValue(name="General", code="G", description="General rules")
    BRANCHES = RuleCategoryValue(name="Branches", code="B", description="Branch rules")
    GITFLOW = RuleCategoryValue(name="GitFlow", code="GF", description="GitFlow rules")
    RULES = RuleCategoryValue(name="Rules", code="R", description="Rules")
    MISC = RuleCategoryValue(
        name="Miscellaneous", code="M", description="Miscellaneous rules"
    )


class RuleStatus(Enum):
    STABLE = "stable"
    UNSTABLE = "unstable"


class BaseRuleConfig(BaseModel):
    """Abstract base rule configuration model."""

    model_config = ConfigDict(extra="forbid")


ConfigT = TypeVar("ConfigT", bound=BaseRuleConfig)

_generic_base = None


# Metaclass to enforce _config presence and type checking
class RuleMeta(ABCMeta):
    def __new__(mcs, name: str, bases: tuple, namespace: dict):
        cls = super().__new__(mcs, name, bases, namespace)

        cls._mutually_exclusive_with_resolved = set()

        if "_name" not in namespace:
            # Determine name from the class name.
            cls._name = camel_to_hyphen(cls.__name__).rstrip("-rule")

        if not isinstance(cls._name, str):
            raise TypeError(
                f"Class {name} must define a '_name' class attribute as a string"
            )

        if "_status" not in namespace:
            cls._status = RuleStatus.STABLE

        if not isinstance(cls._status, RuleStatus):
            raise TypeError(
                f"Class {name} must define a '_status' class attribute as a RuleStatus"
            )

        if "_deprecated" not in namespace:
            cls._deprecated = False

        if not isinstance(cls._deprecated, bool):
            raise TypeError(
                f"Class {name} must define a '_deprecated' class attribute as a bool"
            )

        # Check if fix method is overridden anywhere in the inheritance hierarchy
        cls._fixable = False
        if _generic_base and cls != _generic_base and issubclass(cls, _generic_base):
            base_fix = _generic_base.fix
            cls_fix = cls.fix
            if cls_fix != base_fix:
                cls._fixable = True

        if "_message" not in namespace and hasattr(cls, "_description"):
            cls._message = cls._description

        # Skip validation for the base class itself
        cls._abstract = ABC in bases

        # Get the expected config type from generic parameters
        expected_config_type = BaseRuleConfig
        s = (
            [cls]
            if _generic_base and cls != _generic_base and issubclass(cls, _generic_base)
            else []
        )
        while s:
            klass = s.pop()
            if (
                klass != _generic_base
                and issubclass(klass, _generic_base)
                and hasattr(klass, "__orig_bases__")
            ):
                for orig_base in klass.__orig_bases__:
                    if hasattr(orig_base, "__origin__") and issubclass(
                        orig_base.__origin__, _generic_base
                    ):
                        t = orig_base.__args__[0]
                        if issubclass(t, expected_config_type):
                            expected_config_type = t
                if klass != _generic_base:
                    s.extend(
                        [
                            base
                            for base in klass.__bases__
                            if base != _generic_base and issubclass(base, _generic_base)
                        ]
                    )

        if expected_config_type is None:
            expected_config_type = (
                type(_generic_base._config) if _generic_base else BaseRuleConfig
            )

        cls._configurable = _generic_base and expected_config_type is not type(
            _generic_base._config
        )

        if cls._abstract:
            return cls

        # If no _config is defined, inherit from parent if it's of the expected type.
        if "_config" not in namespace:
            for base in bases:
                if (
                    hasattr(base, "_config")
                    and base._config
                    and issubclass(type(base._config), expected_config_type)
                ):
                    cls._config = base._config
                    break

        # Validate _config existence and type
        if not hasattr(cls, "_config"):
            raise TypeError(f"Class {name} must define a '_config' class attribute")

        if expected_config_type and not isinstance(cls._config, expected_config_type):
            raise TypeError(
                f"Config in {name} must be an instance of {expected_config_type}"
            )

        if "_id" not in namespace:
            raise TypeError(f"Class {name} must define a '_id' class attribute")

        if not isinstance(cls._id, str):
            raise TypeError(
                f"Class {name} must define a '_id' class attribute as a string"
            )

        if "_description" not in namespace:
            raise TypeError(
                f"Class {name} must define a '_description' class attribute"
            )

        if not isinstance(cls._description, str):
            raise TypeError(
                f"Class {name} must define a '_description' class attribute as a string"
            )

        if not hasattr(cls, "_category"):
            cls._category = RuleCategory.MISC

        if not isinstance(cls._category, RuleCategory):
            raise TypeError(
                f"Class {name} must define a '_category' class attribute as a RuleCategory"
            )

        if expected_config_type is not BaseRuleConfig:
            if "_example" not in namespace:
                cls._example = cls._config
        else:
            cls._example = None

        if cls._example is not None and not isinstance(
            cls._example, expected_config_type
        ):
            raise TypeError(
                f"Class {name} must define a '_example' class attribute as {expected_config_type}"
            )

        return cls

    @property
    def rule_id(cls) -> str:
        return cls._id

    @property
    def description(cls) -> str:
        return cls._description


class RuleResult(Enum):
    """Result of a rule check."""

    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class RuleCheckResult:
    """Result of a rule check with details."""

    result: RuleResult
    message: str
    fix_available: bool = False
    fix_description: str | None = None


class Rule(Generic[ConfigT], ABC, metaclass=RuleMeta):  #
    """Base class for all rules."""

    _config = BaseRuleConfig()

    # Class-level set of rule IDs that this rule is mutually exclusive with
    _mutually_exclusive_with: set[str] = set()

    def __init__(self, config: ConfigT | None = None) -> None:
        """
        Initialize with optional config override.

        Args:
            rule_id: Unique identifier for the rule (e.g., 'G001').
            description: Human-readable description of what the rule checks.
            config: If provided, this config instance will be used instead
                of the class-level default config.
        """
        if config is not None:
            self._config = config

    @property
    def config(self) -> ConfigT:
        """Get the configuration (instance-specific or class default)."""
        return self._config

    @property
    def rule_id(self) -> str:
        return type(self).rule_id

    @property
    def description(self) -> str:
        return type(self).description

    @abstractmethod
    def check(self, context: RuleContext) -> RuleCheckResult:
        """Check if the repository complies with this rule.

        Args:
            context: Context object containing all information needed for the check.

        Returns:
            Result of the check with details.
        """
        pass

    def fix(self, context: RuleContext) -> tuple[bool, str]:
        """Apply the fix for this rule.

        This method should only be called if check() returned a RuleCheckResult
        with fix_available=True.

        Args:
            context: Context object containing all information needed for the fix.

        Returns:
            A tuple of (success, message) where success is a boolean indicating if
            the fix was successful, and message provides details about what was done
            or why the fix failed.
        """
        pass


_generic_base = Rule


class RuleSet:
    """A collection of rules that can be applied together."""

    def __init__(self, id: str, description: str):
        """Initialize a rule set.

        Args:
            id: Unique identifier for the rule set (e.g., 'RS001').
            description: Human-readable description of what the rule set checks.
        """
        self._id = id
        self._description = description
        # Store both rules and rule sets in a single list, maintaining order
        self._items: list[Union[type[Rule], "RuleSet"]] = []
        self._mutually_exclusive = dict()

    @property
    def id(self) -> str:
        return self._id

    @property
    def description(self) -> str:
        return self._description

    def add(self, rule: Union[type[Rule], "RuleSet"]) -> None:
        """Add a rule to this rule set.

        Args:
            rule: Rule to add.

        Raises:
            ValueError: If a rule with the same ID already exists.
        """

        if not isinstance(rule, RuleSet) and rule._abstract:
            raise ValueError(f"Rule {rule.rule_id} is abstract.")

        self._items.append(rule)

    def rules(self) -> Iterator[type[Rule]]:
        """Get all rules in this rule set, including those from nested rule sets.

        Rules are returned in the order they were added, with nested rule set rules
        being inserted at the point where the rule set was added.

        Yields:
            Rules in this rule set and all nested rule sets in order of addition.
        """
        rules = []
        for item in self._items:
            if isinstance(item, RuleSet):
                rules.extend(item.rules())
            else:  # Rule
                rules.append(item)

        def remove_dupes(rules):
            seen = set()
            for rule in reversed(rules):
                if rule.rule_id not in seen:
                    seen.add(rule.rule_id)
                    yield rule

        rules = reversed(list(remove_dupes(rules)))

        yield from rules

    def effective_rules(self) -> Iterator[type[Rule]]:
        """Get all rules in this rule set with mutually exclusive rules removed.

        Rules are processed in reverse order (last added first). For each rule,
        any mutually exclusive rules that occur earlier in the list are removed.

        Yields:
            Rules in order, with mutually exclusive rules removed.
        """

        # Get all rules as a list first
        all_rules = list(self.rules())

        # Build up a dictionary of mutually exclusive rules.
        mutually_exclusive_rules = dict()
        for rule in all_rules:
            for id in rule._mutually_exclusive_with:
                mutually_exclusive_rules[rule.rule_id] = mutually_exclusive_rules.get(
                    rule.rule_id, set()
                ) | {id}
                mutually_exclusive_rules[id] = mutually_exclusive_rules.get(
                    id, set()
                ) | {rule.rule_id}

        def filter_exclusive_rules(rules: list[type[Rule]]) -> Iterator[type[Rule]]:
            """Filter out mutually exclusive rules.

            For each rule (processed from the end), removes any earlier rules
            that are mutually exclusive with it.

            Args:
                rules: List of rules to filter

            Yields:
                Rules with mutually exclusive ones removed
            """
            excluded_rules = set()  # Track which rules to exclude

            # Process rules from end to start
            for rule in reversed(rules):
                if rule.rule_id in excluded_rules:
                    continue

                # Include this rule and mark its mutually exclusive rules for exclusion
                excluded_rules.update(mutually_exclusive_rules.get(rule.rule_id, set()))
                yield rule

        # Filter out mutually exclusive rules and reverse back to original order
        yield from reversed(list(filter_exclusive_rules(all_rules)))
