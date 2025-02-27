import * as anchor from "@coral-xyz/anchor";
import { Program } from "@coral-xyz/anchor";
import type { LeeaAgentRegistry } from "../target/types/leea_agent_registry";
import { print_address, log, confirm } from "./utils";
import assert from "assert";
import { Keypair, LAMPORTS_PER_SOL, PublicKey, SystemProgram, Transaction, TransactionMessage, VersionedTransaction } from "@solana/web3.js";

describe("leea-agent-registry", async () => {
    // Configure the client to use the local cluster.
    const provider = anchor.AnchorProvider.env();
    anchor.setProvider(provider);
    const program = anchor.workspace.LeeaAgentRegistry as Program<LeeaAgentRegistry>;
    const connection = provider.connection;

    print_address("🔗 Leea Agent Registry program", program.programId.toString());

    // Create agent keys
    const [agent1, agent2] = Array.from({ length: 2 }, () => Keypair.generate());
    it("Top up agents", async () => {
        let tx = new Transaction();
        tx.instructions = [
            ...[agent1, agent2].map((k) =>
                SystemProgram.transfer({
                    fromPubkey: provider.publicKey,
                    toPubkey: k.publicKey,
                    lamports: 0.01 * LAMPORTS_PER_SOL,
                })
            )];

        await provider.sendAndConfirm(tx).then((t) => log(t, connection));
        const agentBalance1 = await provider.connection.getBalance(agent1.publicKey);
        const agentBalance2 = await provider.connection.getBalance(agent2.publicKey);
        console.log(`Agent1 balance ${agentBalance1}`)
        console.log(`Agent2 balance ${agentBalance2}`)
        assert.equal(agentBalance1, 0.01 * LAMPORTS_PER_SOL)
        assert.equal(agentBalance2, 0.01 * LAMPORTS_PER_SOL)
    });

    it("Register agents", async () => {
        const fee = new anchor.BN(100);
        await program.methods
            .registerAgent("GPT3", "agent to classify text", fee)
            .accounts({
                holder: agent1.publicKey
            })
            .signers([agent1])
            .rpc()
            .then((t) => confirm(t, connection))
            .then((t) => log(t, connection));
        await program.methods
            .registerAgent("DeepSeek", "agent to classify text", fee)
            .accounts({
                holder: agent2.publicKey
            })
            .signers([agent2])
            .rpc()
            .then((t) => confirm(t, connection))
            .then((t) => log(t, connection));

        const [agent1PDA] = anchor.web3.PublicKey.findProgramAddressSync(
            [Buffer.from("leea_agent"), agent1.publicKey.toBuffer()],
            program.programId
        );
        const agent1Data = await program.account.agentAccount.fetch(agent1PDA);
        console.log(`Agent1 name: ${agent1Data.agentName}`)
        console.log(`Agent1 fee: ${agent1Data.fee}`)
        assert.equal(agent1Data.agentName, "GPT3")
        assert.equal(agent1Data.fee, 100)

        const [agent2PDA] = anchor.web3.PublicKey.findProgramAddressSync(
            [Buffer.from("leea_agent"), agent2.publicKey.toBuffer()],
            program.programId
        );
        const agent2Data = await program.account.agentAccount.fetch(agent2PDA);
        console.log(`Agent2 name: ${agent2Data.agentName}`)
        console.log(`Agent2 fee: ${agent2Data.fee}`)
        assert.equal(agent2Data.agentName, "DeepSeek")
        assert.equal(agent2Data.fee, 100)
    });
});