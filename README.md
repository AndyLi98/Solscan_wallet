# Solscan_wallet

Objective: To connect wallets that might have same owner.

Theory: Using https://solscan.io a solana chain explorer one can download a csv file past transaction. Using the transaction we can filter the wallets that send and recieved solana, whats that sends and recieves a certain amount (in this case at least 0.2 solana) are most likely owned by same user.

How it works:
- Go to https://solscan.io and input wallet of choice to search
- Download the the data into csv file
- Under the main function replace "inputwallet" with wallet address that was searched
- replace "SolscanTransfer.csv" with name of csv file
- run the program

