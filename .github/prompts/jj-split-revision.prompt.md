---
agent: jj-parallel-splitter
---
Use the jj-parallel-splitter agent to split revision (@ by default if not specified) into parallel branches. If the user provides specific criteria for splitting, ensure those are followed. Otherwise, analyze the revision's changes and dependencies to determine logical split points that maintain code integrity and functionality.