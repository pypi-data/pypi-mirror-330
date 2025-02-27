use anchor_lang::prelude::*;
mod contexts;
use contexts::*;
mod states;

declare_id!("Ej5xSQCEJmXUEjrPV37ZEXrvRiRbUdunbZH4yoZfcg2s");
#[program]
pub mod escrow {
    use super::*;

    pub fn initialize(ctx: Context<Initialize>) -> Result<()> {
        ctx.accounts.initialize_escrow(&ctx.bumps)
    }

    pub fn deposit(ctx: Context<Deposit>, amount: u64) -> Result<()> {
        ctx.accounts.deposit(amount)
    }

    pub fn cancel(ctx: Context<Cancel>) -> Result<()> {
        ctx.accounts.refund_and_close_vault()
    }

    pub fn pay_to_agent(ctx: Context<Pay>, amount: u64) -> Result<()> {
        ctx.accounts.pay_to_agent(amount)
    }
}
