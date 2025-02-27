use anchor_lang::prelude::*;
use anchor_spl::{
    associated_token::AssociatedToken,
    token::{
        close_account, transfer_checked, CloseAccount, Mint, Token, TokenAccount, TransferChecked,
    },
};

use crate::global::ADMIN_PUBKEY;
use crate::states::Escrow;

#[derive(Accounts)]
#[instruction(amount: u64)]
pub struct Pay<'info> {
    #[account(mut,address = ADMIN_PUBKEY)]
    pub admin: Signer<'info>,
    #[account(mut)]
    pub taker: AccountInfo<'info>,
    #[account(mut)]
    pub initializer: AccountInfo<'info>,
    pub mint_a: Box<Account<'info, Mint>>,
    #[account(
        init_if_needed,
        payer = admin,
        associated_token::mint = mint_a,
        associated_token::authority = taker
    )]
    pub taker_ata_a: Box<Account<'info, TokenAccount>>,
    #[account(
        mut,
        has_one = mint_a,
        seeds=[b"state", initializer.key().as_ref()],
        bump = escrow.bump
    )]
    pub escrow: Box<Account<'info, Escrow>>,
    #[account(
        mut,
        constraint = vault.amount >= amount,
        associated_token::mint = mint_a,
        associated_token::authority = escrow
    )]
    pub vault: Box<Account<'info, TokenAccount>>,
    pub associated_token_program: Program<'info, AssociatedToken>,
    pub token_program: Program<'info, Token>,
    pub system_program: Program<'info, System>,
}

impl<'info> Pay<'info> {
    pub fn pay_to_agent(&mut self, amount: u64) -> Result<()> {
        let signer_seeds: [&[&[u8]]; 1] = [&[
            b"state",
            &self.initializer.key().to_bytes()[..],
            &[self.escrow.bump],
        ]];

        transfer_checked(
            self.into_withdraw_context().with_signer(&signer_seeds),
            amount,
            self.mint_a.decimals,
        )
        // close_account(self.into_close_context().with_signer(&signer_seeds))
    }

    fn into_withdraw_context(&self) -> CpiContext<'_, '_, '_, 'info, TransferChecked<'info>> {
        let cpi_accounts = TransferChecked {
            from: self.vault.to_account_info(),
            mint: self.mint_a.to_account_info(),
            to: self.taker_ata_a.to_account_info(),
            authority: self.escrow.to_account_info(),
        };
        CpiContext::new(self.token_program.to_account_info(), cpi_accounts)
    }

    // fn into_close_context(&self) -> CpiContext<'_, '_, '_, 'info, CloseAccount<'info>> {
    //     let cpi_accounts = CloseAccount {
    //         account: self.vault.to_account_info(),
    //         destination: self.initializer.to_account_info(),
    //         authority: self.escrow.to_account_info(),
    //     };
    //     CpiContext::new(self.token_program.to_account_info(), cpi_accounts)
    // }
}
