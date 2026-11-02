Output raw4.mp4
Set Shell "bash"
Set FontSize 18
Set Width 1000
Set Height 1180
Set Padding 28
Set Theme "Catppuccin Mocha"
Set TypingSpeed 40ms

Hide
Type "source ./wrap2.sh && clear"
Enter
Sleep 800ms
Show

Type "# A real PR of mine: opt-in Redis caching (+173 -2)"
Enter
Sleep 1200ms
Type "claude -p 'good-code-review: review redis-cache vs main, ledger only'"
Sleep 800ms
Enter
Wait@120s /^\$$/
Sleep 12s
