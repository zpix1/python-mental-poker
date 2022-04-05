Client:
1. Set up items and parameters (N strings, k - cards for each side, 2*k <= N)
2. Init crypto values (p, c, d, string values)
3. Send them to server
4. Encrypt values, shuffle them and send them to the server
5. Get **client** deck from server (k c-encrypted strings)
6. Get s-encrypted n-k strings from server
7. Select k s-encrypted strings and send them to the server
8. **Well done**