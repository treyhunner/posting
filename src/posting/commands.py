from functools import partial
from typing import TYPE_CHECKING, cast
from textual.command import DiscoveryHit, Hit, Hits, Provider
from textual.types import IgnoreReturnCallbackType

if TYPE_CHECKING:
    from posting.app import Posting


class PostingProvider(Provider):
    @property
    def commands(
        self,
    ) -> tuple[tuple[str, IgnoreReturnCallbackType, str], ...]:
        app = self.posting
        return (
            (
                "layout: horizontal",
                partial(app.command_layout, "horizontal"),
                "Change layout to horizontal",
            ),
            (
                "layout: vertical",
                partial(app.command_layout, "vertical"),
                "Change layout to vertical",
            ),
            *self.get_theme_commands(),
        )

    async def discover(self) -> Hits:
        """Handle a request for the discovery commands for this provider.

        Yields:
            Commands that can be discovered.
        """
        for name, runnable, help_text in self.commands:
            yield DiscoveryHit(
                name,
                runnable,
                help=help_text,
            )

    async def search(self, query: str) -> Hits:
        """Handle a request to search for commands that match the query.

        Args:
            query: The user input to be matched.

        Yields:
            Command hits for use in the command palette.
        """
        matcher = self.matcher(query)
        for name, runnable, help_text in self.commands:
            if (match := matcher.match(name)) > 0:
                yield Hit(
                    match,
                    matcher.highlight(name),
                    runnable,
                    help=help_text,
                )

    def get_theme_commands(
        self,
    ) -> tuple[tuple[str, IgnoreReturnCallbackType, str], ...]:
        posting = self.posting
        return tuple(self.get_theme_command(theme) for theme in posting.themes)

    def get_theme_command(
        self, theme_name: str
    ) -> tuple[str, IgnoreReturnCallbackType, str]:
        return (
            f"theme: {theme_name}",
            partial(self.posting.command_theme, theme_name),
            f"Set the theme to {theme_name}",
        )

    @property
    def posting(self) -> "Posting":
        return cast("Posting", self.screen.app)


# """A command palette command provider for Textual system commands.

# This is a simple command provider that makes the most obvious application
# actions available via the [command palette][textual.command.CommandPalette].
# """

# from __future__ import annotations

# from .command import DiscoveryHit, Hit, Hits, Provider
# from .types import IgnoreReturnCallbackType


# class SystemCommands(Provider):
#     """A [source][textual.command.Provider] of command palette commands that run app-wide tasks.

#     Used by default in [`App.COMMANDS`][textual.app.App.COMMANDS].
#     """

#     @property
#     def _system_commands(self) -> tuple[tuple[str, IgnoreReturnCallbackType, str], ...]:
#         """The system commands to reveal to the command palette."""
#         return (
#             (
#                 "Toggle light/dark mode",
#                 self.app.action_toggle_dark,
#                 "Toggle the application between light and dark mode",
#             ),
#             (
#                 "Quit the application",
#                 self.app.action_quit,
#                 "Quit the application as soon as possible",
#             ),
#             (
#                 "Ring the bell",
#                 self.app.action_bell,
#                 "Ring the terminal's 'bell'",
#             ),
#         )

#     async def discover(self) -> Hits:
#         """Handle a request for the discovery commands for this provider.

#         Yields:
#             Commands that can be discovered.
#         """
#         for name, runnable, help_text in self._system_commands:
#             yield DiscoveryHit(
#                 name,
#                 runnable,
#                 help=help_text,
#             )

#     async def search(self, query: str) -> Hits:
#         """Handle a request to search for system commands that match the query.

#         Args:
#             query: The user input to be matched.

#         Yields:
#             Command hits for use in the command palette.
#         """
#         # We're going to use Textual's builtin fuzzy matcher to find
#         # matching commands.
#         matcher = self.matcher(query)

#         # Loop over all applicable commands, find those that match and offer
#         # them up to the command palette.
#         for name, runnable, help_text in self._system_commands:
#             if (match := matcher.match(name)) > 0:
#                 yield Hit(
#                     match,
#                     matcher.highlight(name),
#                     runnable,
#                     help=help_text,
#                 )
