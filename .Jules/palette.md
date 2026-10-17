## 2024-05-18 - Friendly Empty States & Error Handling in CLI Bots
**Learning:** For terminal or chat-based bots, generic outputs like `1. ` or unhandled exceptions significantly degrade UX. Providing context-aware success messages ("Added 'xyz'") and clear error guidance makes a text interface feel robust and user-friendly.
**Action:** Always validate input boundaries and arrays indices. Add friendly empty states instead of raw empty values. Use the user's input in the feedback loop to confirm actions.
