"""Core linting functionality."""


import colorama
from colorama import Fore, Style
from github.Repository import Repository

from lintr.config import BaseLintrConfig, RepositoryConfig
from lintr.rule_manager import RuleManager
from lintr.rules import RuleCheckResult, RuleResult, RuleSet
from lintr.rules.context import RuleContext

# Initialize colorama for cross-platform color support
colorama.init()


class Linter:
    """Core linting functionality."""

    def __init__(
        self,
        config: BaseLintrConfig,
        dry_run: bool = False,
        non_interactive: bool = False,
        fix: bool = False,
    ):
        """Initialize the linter.

        Args:
            config: Lintr configuration.
            dry_run: If True, no changes will be made.
            non_interactive: If True, apply fixes without prompting for confirmation.
            fix: If True, attempt to fix issues automatically.
        """
        self._config = config
        self._dry_run = dry_run
        self._non_interactive = non_interactive
        self._fix = fix
        self._rule_manager = RuleManager(config.rules, config.rulesets)

    def create_context(self, repository: Repository) -> RuleContext:
        """Create a rule context for a repository.

        Args:
            repository: GitHub repository to create context for.

        Returns:
            Rule context for the repository.
        """
        return RuleContext(repository=repository, dry_run=self._dry_run)

    def get_rule_set_for_repository(
        self, repository_config: RepositoryConfig | None
    ) -> tuple[str, RuleSet] | None:
        """Get the rule set to use for a repository.

        The rule set is determined in the following order:
        1. Repository-specific rule set from configuration
        2. Default rule set from configuration

        Args:
            repository: GitHub repository to get rule set for.

        Returns:
            Tuple of (rule set ID, rule set) if found, None otherwise.
        """
        # Check for repository-specific rule set
        if repository_config:
            rule_set_id = repository_config.ruleset
            if rule_set_id:
                rule_set = self._rule_manager.get(rule_set_id)
                if rule_set and isinstance(rule_set, RuleSet):
                    return rule_set_id, rule_set

        # Fall back to default rule set
        if self._config.default_ruleset:
            rule_set = self._rule_manager.get(self._config.default_ruleset)
            if rule_set and isinstance(rule_set, RuleSet):
                return self._config.default_ruleset, rule_set

        return None

    def check_repository(
        self,
        repository: Repository,
        rule_set: RuleSet,
        repository_config: RepositoryConfig | None = None,
    ) -> dict[str, RuleCheckResult]:
        """Check a repository against all rules in a rule set.

        Args:
            repository: GitHub repository to check.
            rule_set: Rule set to use for checking.

        Returns:
            Dictionary mapping rule IDs to their check results.
        """
        context = self.create_context(repository)
        results = {}

        for rule in rule_set.effective_rules():
            rule_config = (
                repository_config.rules.get(rule.rule_id) if repository_config else None
            )
            if rule_config:
                rule = rule(type(rule._config).model_validate(rule_config))
            else:
                rule = rule()
            result = None
            try:
                result = rule.check(context)
                results[rule.rule_id] = result
            except Exception as e:
                print(
                    f"{Fore.RED}Error executing rule {rule.rule_id} on repository {repository.name}: {str(e)}{Style.RESET_ALL}"
                )
                result = RuleCheckResult(
                    result=RuleResult.FAILED,
                    message=f"Rule execution failed: {str(e)}",
                    fix_available=False,
                )
                results[rule.rule_id] = result

            # Print rule result
            if result.result == RuleResult.PASSED:
                status_symbol = f"{Fore.GREEN}✓{Style.RESET_ALL}"
            elif result.result == RuleResult.FAILED:
                status_symbol = f"{Fore.RED}✗{Style.RESET_ALL}"
            else:  # SKIPPED
                status_symbol = f"{Fore.YELLOW}-{Style.RESET_ALL}"

            print(f"  {status_symbol} {rule.rule_id}: {result.message}")

            # Always show fix description if available
            if result.fix_available:
                print(f"    {Fore.BLUE}⚡ {result.fix_description}{Style.RESET_ALL}")

                # Only proceed with fix if --fix flag is provided
                if self._fix:
                    if self._dry_run:
                        print(
                            f"    {Fore.YELLOW}ℹ Would attempt to fix this issue (dry run){Style.RESET_ALL}"
                        )
                    else:
                        try:
                            should_fix = self._non_interactive

                            if not self._non_interactive:
                                response = input(
                                    f"    {Fore.YELLOW}ℹ Apply this fix? [y/N]: {Style.RESET_ALL}"
                                ).lower()
                                should_fix = response in ["y", "yes"]

                            if should_fix:
                                success, message = rule.fix(context)
                                if success:
                                    print(
                                        f"    {Fore.GREEN}⚡ Fixed: {message}{Style.RESET_ALL}"
                                    )
                                    # Re-run check to get updated status
                                    result = rule.check(context)
                                    results[rule.rule_id] = result
                                    # Re-display rule status
                                    if result.result == RuleResult.PASSED:
                                        status_symbol = (
                                            f"{Fore.GREEN}✓{Style.RESET_ALL}"
                                        )
                                    elif result.result == RuleResult.FAILED:
                                        status_symbol = f"{Fore.RED}✗{Style.RESET_ALL}"
                                    else:  # SKIPPED
                                        status_symbol = (
                                            f"{Fore.YELLOW}-{Style.RESET_ALL}"
                                        )
                                    print(
                                        f"  {status_symbol} {rule.rule_id}: {result.message}"
                                    )
                                else:
                                    print(
                                        f"    {Fore.RED}⚡ Fix failed: {message}{Style.RESET_ALL}"
                                    )
                            else:
                                print(
                                    f"    {Fore.YELLOW}ℹ Fix skipped{Style.RESET_ALL}"
                                )
                        except Exception as e:
                            print(
                                f"    {Fore.RED}⚡ Fix error: {str(e)}{Style.RESET_ALL}"
                            )

        return results

    def lint_repositories(
        self, repositories: list[Repository]
    ) -> dict[str, dict[str, RuleCheckResult]]:
        """Lint a list of repositories.

        Args:
            repositories: List of GitHub repositories to lint.

        Returns:
            Dictionary mapping repository names to their lint results.
            Each lint result is a dictionary mapping rule IDs to their check results.
        """
        results = {}

        for repo in repositories:
            # Get the config for the repository.
            repo_config = self._config.repositories.get(repo.name)
            # Get rule set for repository
            rule_set_info = self.get_rule_set_for_repository(repo_config)
            if not rule_set_info:
                print(f"{Fore.YELLOW}- {repo.name} (no rule set){Style.RESET_ALL}")
                results[repo.name] = {"error": "No rule set found for repository"}
                continue

            rule_set_id, rule_set = rule_set_info
            print(f"{Fore.WHITE}- {repo.name} ({rule_set_id}){Style.RESET_ALL}")

            # Run all rules in the rule set
            try:
                rule_results = self.check_repository(repo, rule_set, repo_config)
                results[repo.name] = rule_results
            except Exception as e:
                print(f"{Fore.RED}  Error: {str(e)}{Style.RESET_ALL}")
                results[repo.name] = {"error": f"Failed to check repository: {str(e)}"}

        return results
