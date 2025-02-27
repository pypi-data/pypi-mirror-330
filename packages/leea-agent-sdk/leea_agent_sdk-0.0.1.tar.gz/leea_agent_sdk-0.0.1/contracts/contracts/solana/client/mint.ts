import BN from "bn.js";
import * as anchor from "@coral-xyz/anchor";
import { Program } from "@coral-xyz/anchor";
import * as web3 from "@solana/web3.js";
import type { LeeaTokenAico } from "../target/types/leea_token_aico";
import { print_address, log, confirm } from "../tests/utils";
import { Keypair, LAMPORTS_PER_SOL } from "@solana/web3.js";
import path from 'path'
import { getAssociatedTokenAddressSync } from "@solana/spl-token";
import { Connection } from "@solana/web3.js";
import NodeWallet from "@coral-xyz/anchor/dist/cjs/nodewallet";

// Connect to solana
// 1. Admin key
let fullPath = path.resolve(process.cwd(), '../solana/tests/admin.json')
let secret = require(fullPath)
if (!secret) {
    throw new Error(`No secret found at ${fullPath}`)
}
const adminKey = Keypair.fromSecretKey(new Uint8Array(secret))
console.log(`Admin key: ${adminKey.publicKey.toString()}'`); // GB9XNqUC32ZibLza8d7qMKBEv1hPZ142hzZ3sju7hG7b

const wallet = new NodeWallet(Keypair.fromSecretKey(new Uint8Array(secret)));
const solanaConnection = new Connection("https://api.devnet.solana.com", "confirmed");
const provider = new anchor.AnchorProvider(solanaConnection, wallet, {
    commitment: "processed",
});
anchor.setProvider(provider);
const program = anchor.workspace.LeeaTokenAico as Program<LeeaTokenAico>;
const connection = provider.connection;
print_address("🔗 Leea aiCO program", program.programId.toString());

const receiverPubKey = new web3.PublicKey(
    "GySEf7vywsNKkWEN8s1K467Cuf5e6j51kXwyaJvfkrMg"
);

const [leeaTokenMintPDA] = anchor.web3.PublicKey.findProgramAddressSync(
    [Buffer.from("aiCO_reward")],
    program.programId
);

const receiverTokenAccount = getAssociatedTokenAddressSync(
    leeaTokenMintPDA,
    receiverPubKey
);
async function main() {
    await program.methods
        .mintToReceiver(new BN(100 * LAMPORTS_PER_SOL))
        .accounts({
            // @ts-ignore
            admin: adminKey.publicKey,
            leeaTokenMint: leeaTokenMintPDA,
            receiver: receiverPubKey,
            receiverTokenAccount: receiverTokenAccount
        })
        .signers([adminKey])
        .rpc()
        .then((t) => confirm(t, connection))
        .then((t) => log(t, connection));
    const receiverBalance = await provider.connection.getTokenAccountBalance(receiverTokenAccount)
    console.log("Receiver Token Balance: ", receiverBalance.value.uiAmount);
}

main()
