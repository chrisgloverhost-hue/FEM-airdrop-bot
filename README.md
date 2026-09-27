# Telegram Airdrop Bot

This bot has all you need and very simple to use!
### Some of the great futures

- Collect FEM app, X, TikTok follow/like, and Telegram task claims for admin review.
- Pay approved participants 40 native FEM on the FEM Besu EVM chain and announce successful transactions in Telegram.
- Check if a correct wallet address has been provided
- Very easy to use.
- Persistance, the chat will remain persistant even if you restart the bot.
- Blocks duplicate wallets & twitter usernames
- Refferal support
- Start, stop, pause airdrop anytime.
- Captcha support

### Admin Commands

- `/list` Returns the list of all participants in json format.
- `/stats` Returns number of participants, referrals, distribution amounts
- `/bot stop|pause|start` Manage airdrop status; stop, pause or start.
- `/pending` Lists participants awaiting payout review, including their submitted task handles and wallet.
- `/approve <telegram_user_id>` Sends one 40 FEM payout to the participant and posts their full wallet and transaction hash/link to the announcement group.
- `/retryannouncements` Retries Telegram announcements for payouts already confirmed on-chain.
- `/announce <message>` Posts a campaign update to the same announcement group.

Payout and announcement commands only work in a private chat with the configured `ADMIN_USERNAME`. `/pending` shows saved claims for app setup, Telegram, X, TikTok follow, and TikTok likes. These actions are self-reported; the bot does not automatically verify app installation, Telegram membership, or X/TikTok activity. `/approve` broadcasts an irreversible on-chain transfer, so review task claims and the wallet before approving.

Campaign cap: `500000` participants × `40` FEM each = `20000000` FEM total. Set `MAX_USERS=500000` and keep `REFERRAL_REWARD=0` to keep the pool at 20 million FEM. You can also post directly in the Telegram group if your account has posting rights there.

## Railway Deployment
- Create a Railway project from this GitHub repository and deploy it using the included Dockerfile.
- Add a Railway MongoDB service and set `MONGO_URI` to its private connection URL.
- Set the environment variables below in Railway. Replace the empty campaign URLs with official links.
- Add the bot as an administrator in the Telegram announcement group and set `FEM_ANNOUNCEMENT_CHAT_ID` to its chat ID.
- Send `/announce Your campaign update` to the bot in a private chat to post updates through the bot.
- Start with `FEM_PAYOUT_ENABLED=NO`. Verify the RPC URL, chain ID, decimals, wallet balance, recipient, and test transaction before enabling payouts.
- Run one bot replica because it uses Telegram long polling. No public domain or webhook is required.

For local Docker Compose, copy `.env.example` to `.env`, provide valid Telegram and campaign links, and configure the MongoDB variables.

## Railway Variables

- `BOT_TOKEN`: Telegram Bot API token from BotFather. Store as a Railway secret.
- `ADMIN_USERNAME`: Telegram username allowed to review and approve payouts.
- `MONGO_URI`: Railway MongoDB connection URL. Prefer this over the local `MONGO_INITDB_*` variables.
- `FEM_APP_LINK`: Official FEM app download/setup URL.
- `TWITTER_LINKS`: Comma-separated X profile URLs.
- `TIKTOK_LINKS`: Comma-separated TikTok profile URLs.
- `TIKTOK_VIDEO_LINKS`: Comma-separated TikTok post URLs participants must follow/like.
- `TELEGRAM_LINKS`: Comma-separated public invite links displayed to participants.
- `FEM_REWARD_AMOUNT`: Native FEM amount per approved participant; set to `40`.
- `FEM_DECIMALS`: Native FEM precision; typically `18`, but confirm with the FEM chain operators.
- `FEM_RPC_URL`: Besu JSON-RPC endpoint reachable from Railway.
- `FEM_CHAIN_ID`: Exact integer chain ID returned by the FEM RPC endpoint.
- `FEM_PAYOUT_PRIVATE_KEY`: Dedicated, funded payout wallet private key. Add only as a Railway secret; never commit it or put it in chat. Keep only campaign funds and gas needed in this hot wallet.
- `FEM_PAYOUT_ENABLED`: Must remain `NO` until chain configuration and a test transfer are confirmed; set `YES` to enable `/approve` transfers.
- `FEM_ANNOUNCEMENT_CHAT_ID`: Telegram group chat ID for public payout announcements. The bot must be an administrator with permission to post. Payout approval is blocked until configured.
- `FEM_TX_EXPLORER_URL`: Optional transaction URL prefix ending in `/`, used to make announcement links.
- `AIRDROP_AMOUNT`: Legacy setting; the displayed and transferred participant reward comes from `FEM_REWARD_AMOUNT` (`40`).
- `COIN_SYMBOL`: `FEM`.
- `COIN_NAME`: `FEM`.
- `AIRDROP_NETWORK`: `FEM EVM (Besu)`.
- `AIRDROP_DATE`, `COIN_PRICE`, `REFERRAL_REWARD`, `WEBSITE_URL`, `EXPLORER_URL`, `MAX_USERS`, `MAX_REFS`, and `CAPTCHA_ENABLED`: Existing campaign settings.

The included `.env.example` intentionally leaves official campaign links and live chain details empty. The application refuses to start without the FEM app, X, TikTok, and TikTok video links. Confirm the FEM RPC is the correct production chain before setting `FEM_PAYOUT_ENABLED=YES`.

## Local Docker Compose
The local Docker Compose setup can use the `MONGO_INITDB_*` variables instead of `MONGO_URI`; run `docker-compose up -d` after configuring `.env`.

## Other Campaign Settings

- `COIN_SYMBOL` Is the coin symbol
    - Example: `BNB, ETH`
- `COIN_NAME` Is the coin name
    - Example: `Bitcoin, Ethereum`
- `AIRDROP_AMOUNT` How many tokens are you going to give
    - Example: `10000` *do not* include "," must be float number
- `AIRDROP_DATE` Date of reward distrubition
    - Example: `20 July 2021`
- `BOT_TOKEN` The token you get from @BotFather
    - Example: `1313552295:AAFxDGKhlco-FoWw-uyxInotlKvalidNEz-Q`
- `COIN_PRICE` Current price of coin
    - Example: `$0.01`
- `REFERRAL_REWARD` Extra reward participants will get for each referral
    - Example: `1000`
- `WEBSITE_URL` Your website url
    - Example: `https://bitcoin.com`
- `EXPLORER_URL` Blockchain explorer url
    - Example: `https://etherscan.io/address/0x0000000000000000000000000000000000000000`
- `ADMIN_USERNAME` Your telegram username
    - Example: `johnboe`
- `MAX_USERS` Maximum number of participants
    - Example: `1000` *do not* include "," must be float number
- `MAX_REFS` Maximum number of referrals per participant
    - Example: `5`
- `CAPTCHA_ENABLED` Enable or disable captcha at start
    - Example: `YES` or `NO`
- `TWITTER_LINKS` Twitter page links seperated by comma
    - Example: `https://twitter.com/bitcoin,`
    - Example: `https://twitter.com/bitcoin,https://twitter.com/ethereum`
- `TIKTOK_LINKS` TikTok profile links separated by comma. Users must follow the profiles and provide their TikTok username.
    - Example: `https://www.tiktok.com/@exampleaddress`
- `TELEGRAM_LINKS` Telegram group links seperated by comma
    - Example: `https://t.me/single,`
    - Example: `https://t.me/multi,https://t.me/ple`


### Not Very Important

Leave these to default unless you know what you do.

- `MONGO_INITDB_ROOT_USERNAME` Mongodb username
- `MONGO_INITDB_ROOT_USERNAME` Mongodb password
- `MONGO_INITDB_IP` Mongodb IP
- `MONGO_INITDB_PORT` Mongodb Port

## Some Screenshots
![1](./images/1.jpg)
![1](./images/2.jpg)
