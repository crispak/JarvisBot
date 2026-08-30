## 2024-08-30 - Empty States matter for chat bots too
**Learning:** Even in text-based bot interfaces, empty states and handling trailing symbols string parsing can easily break the UI output. Returning an empty text or string with newlines is bad UX.
**Action:** Always verify what the default returned state is when lists or storage are empty.
