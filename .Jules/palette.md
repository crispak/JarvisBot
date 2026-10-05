## 2023-11-20 - Friendly Empty States and List Cleanups
**Learning:** Even in backend text bots, trailing delimiters caused by simple splits can create weird formatting like empty bullet points (`3. `). Also, empty data states without guidance can leave users feeling stuck.
**Action:** When parsing stored lists, ensure empty trailing entries are filtered out. Provide helpful empty states ("Your list is empty. Do X to add one!") to make the bot more conversational and guide users effectively.
