use anchor_lang::prelude::*;

#[account]
pub struct Escrow {
    pub bump: u8,
    pub initializer: Pubkey,
    pub mint_a: Pubkey,
}

impl Space for Escrow {
    // First 8 Bytes are Discriminator (u64)
    const INIT_SPACE: usize = 8 + 8 + 1 + 32 + 32;
}