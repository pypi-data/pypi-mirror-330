use anchor_lang::prelude::*;
use solana_program::{pubkey, pubkey::Pubkey};

declare_id!("DM24Huh1FZ3SG3VxBYNqeePG9Vmnze9MdonghHeTPEzG");

const ADMIN_PUBKEY: Pubkey = pubkey!("GB9XNqUC32ZibLza8d7qMKBEv1hPZ142hzZ3sju7hG7b");
const AGENT_SEED: &[u8] = b"leea_agent";

#[program]
pub mod leea_agent_registry {
    use super::*;
    pub fn register_agent(
        ctx: Context<RegisterAgent>,
        agent_name: String,
        description: String,
        fee: u64,
    ) -> Result<()> {
        let holder = &ctx.accounts.holder;
        let agent_account = &mut ctx.accounts.agent_account;
        agent_account.holder = *holder.key;
        agent_account.agent_name = agent_name;
        agent_account.description = description;
        agent_account.fee = fee;
        agent_account.created_at = Clock::get().unwrap().unix_timestamp;
        Ok(())
    }

    pub fn update_agent_score(ctx: Context<UpdateAgentScore>, score: u64) -> Result<()> {
        let agent_account = &mut ctx.accounts.agent_account;
        agent_account.score = score;
        agent_account.updated_at = Clock::get().unwrap().unix_timestamp;
        Ok(())
    }
}

#[derive(Accounts)]
pub struct RegisterAgent<'info> {
    #[account(mut)]
    pub holder: Signer<'info>,
    #[account(
        init,
        payer = holder,
        seeds = [AGENT_SEED, holder.key().as_ref()],
        bump,
        space = 8 + std::mem::size_of::<AgentAccount>(),
    )]
    pub agent_account: Account<'info, AgentAccount>,
    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct UpdateAgentScore<'info> {
    #[account(mut,address = ADMIN_PUBKEY)]
    pub admin: Signer<'info>,

    #[account(mut)]
    pub holder: AccountInfo<'info>,

    #[account(
        mut,
        seeds = [AGENT_SEED, holder.key().as_ref()],
        bump,
    )]
    pub agent_account: Account<'info, AgentAccount>,
    pub system_program: Program<'info, System>,
}

#[account]
#[derive(Default)]
pub struct AgentAccount {
    pub holder: Pubkey,
    pub agent_name: String,
    pub description: String,
    pub fee: u64,
    pub score: u64,
    pub created_at: i64,
    pub updated_at: i64,
}
