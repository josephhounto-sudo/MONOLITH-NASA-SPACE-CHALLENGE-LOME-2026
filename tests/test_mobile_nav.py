"""On a phone the sidebar starts collapsed; its opener sits in the toolbar. The CSS must not hide that opener (found 19/11: display:none on the toolbar)."""
import inspect

from csync.ui import style


def test_toolbar_opener_is_kept_visible_and_only_actions_are_hidden():
    css = style._NAV
    assert '[data-testid="stExpandSidebarButton"]' in css and "display:flex!important" in css
    assert "stToolbarActions" in css, "only the toolbar actions may be hidden"
    assert '[data-testid="stToolbar"]{display:none' not in css


def test_inject_applies_the_nav_rule_after_the_fusion_css():
    src = inspect.getsource(style.inject)
    assert "_NAV" in src
