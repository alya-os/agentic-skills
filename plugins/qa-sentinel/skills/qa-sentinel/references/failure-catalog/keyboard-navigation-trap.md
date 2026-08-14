# keyboard-navigation-trap

## Description
A keyboard-only user can enter a UI element (modal, dropdown, custom widget) but cannot exit it via keyboard. Focus is trapped. The user has no way to recover except mouse or page reload.

## Symptoms
- Tab inside a modal cycles forever; Escape doesn't close it
- Custom dropdown captures arrow keys but not Escape
- Focus moves into a third-party widget (chat, video) and cannot return
- After closing a modal, focus is lost (lands on body, not the trigger)
- Skip-link exists but doesn't work

## Root cause
Custom widgets implemented without keyboard contract: trap focus on open, restore focus on close, support Escape to dismiss, return focus to trigger.

## Independent verification
Use `agent-browser` to send Tab and Shift+Tab through every interactive surface. Open every modal, dropdown, accordion, and custom widget. Verify Escape closes them. Verify focus returns to the trigger.

For third-party widgets, document the trap and require a workaround if the widget cannot be fixed.

## Common fix attempts that DON'T work
- Adding `tabindex="-1"` everywhere (breaks legitimate focus)
- Disabling the widget on mobile (doesn't help keyboard users on desktop)
- Adding a close button (doesn't help if Escape is also broken)

The fix that works: implement the full keyboard contract on every custom widget. Use established patterns (focus-trap libraries, ARIA dialog patterns).

## Likely lenses
accessibility
