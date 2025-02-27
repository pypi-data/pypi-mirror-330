import * as anchor from "@coral-xyz/anchor";
import { Escrow } from "../target/types/escrow";
import { Keypair, LAMPORTS_PER_SOL, PublicKey, SystemProgram } from "@solana/web3.js";
import {
    ASSOCIATED_TOKEN_PROGRAM_ID,
    TOKEN_PROGRAM_ID,
    getAssociatedTokenAddressSync
} from "@solana/spl-token";
import { randomBytes } from "crypto";
import * as web3 from "@solana/web3.js";
import path from 'path'
import assert from "assert";
import { log, confirm, print_address } from "../tests/utils";
import NodeWallet from "@coral-xyz/anchor/dist/cjs/nodewallet";
import type { LeeaTokenAico } from "../target/types/leea_token_aico";
import bs58 from 'bs58';

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
const solanaConnection = new web3.Connection("https://api.devnet.solana.com", "confirmed");
const provider = new anchor.AnchorProvider(solanaConnection, wallet, {
    commitment: "processed",
});
anchor.setProvider(provider);
const program = anchor.workspace.Escrow as anchor.Program<Escrow>;
const connection = provider.connection;
const leeaAiCOprogram = anchor.workspace.LeeaTokenAico as anchor.Program<LeeaTokenAico>;
print_address("🔗 Leea Escrow program", program.programId.toString());


const [leeaTokenMintPDA] = anchor.web3.PublicKey.findProgramAddressSync(
    [Buffer.from("aiCO_reward")],
    leeaAiCOprogram.programId
);

const secretKey = bs58.decode("2eP88GfSJwGWEn1feXvzx2b6c6Dp2VmABUgyjkPguSgPmkvzrwz5eFhkAAsVMaeY1PFTC68Dh4uPFVJ3UCUkuL58"); // private key from Phantom
const initializer = Keypair.fromSecretKey(secretKey);
console.log(`Initializer key: ${initializer.publicKey.toString()}'`);

// Initializer Token account
const initializerAtaA = getAssociatedTokenAddressSync(leeaTokenMintPDA, initializer.publicKey)

// Determined Escrow and Vault addresses
const escrow = PublicKey.findProgramAddressSync(
    [Buffer.from("state"), initializer.publicKey.toBuffer()],
    program.programId
)[0];
const vault = getAssociatedTokenAddressSync(leeaTokenMintPDA, escrow, true);

const accounts = {
    admin: adminKey.publicKey,
    initializer: initializer.publicKey,
    mintA: leeaTokenMintPDA,
    initializerAtaA: initializerAtaA,
    escrow,
    vault,
    associatedTokenprogram: ASSOCIATED_TOKEN_PROGRAM_ID,
    tokenProgram: TOKEN_PROGRAM_ID,
    systemProgram: SystemProgram.programId,
};

async function main() {
    let initializerBalance = await provider.connection.getTokenAccountBalance(
        initializerAtaA
    );
    console.log("Initializer token balance before escrowing: ", initializerBalance.value.amount.toString());
    const initializerAmount = 1 * LAMPORTS_PER_SOL;
    await program.methods
        .initialize()
        .accounts({ ...accounts })
        .signers([initializer])
        .rpc()
        .then((t) => confirm(t, connection))
        .then((t) => log(t, connection));

    await program.methods
        .deposit(new anchor.BN(initializerAmount))
        .accounts({ ...accounts })
        .signers([initializer])
        .rpc()
        .then((t) => confirm(t, connection))
        .then((t) => log(t, connection));

    initializerBalance = await provider.connection.getTokenAccountBalance(
        initializerAtaA
    );
    console.log("Initializer token balance after escrowing: ", initializerBalance.value.amount.toString());
    let vaultBalance = await provider.connection.getTokenAccountBalance(
        vault
    );
    console.log("Vault token balance: ", vaultBalance.value.amount.toString());
    assert.equal(vaultBalance.value.amount, initializerAmount)
}

main()