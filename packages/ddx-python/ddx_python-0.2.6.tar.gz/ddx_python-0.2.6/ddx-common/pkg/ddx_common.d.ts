/* tslint:disable */
/* eslint-disable */
// Debit/credit to the trader's account coming from fees and realized p&l
export type LedgerEntry = { fee: BigNumber; ddxFeeElection: boolean; realizedPnl: BigNumber };

// Info about a single pair of matched orders filled
export type Fill = {
    symbol: string;
    takerOrderHash: DataHexString;
    makerOrderHash: DataHexString;
    amount: BigNumber;
    price: BigNumber;
    takerLedgerEntry: LedgerEntry;
    collateralToken: Address;
};

// Order posted to the book but did not take
export type Post = { symbol: string; orderHash: DataHexString; amount: BigNumber };

// Order canceled and removed from the book but did not take
export type Cancel = { symbol: string; orderHash: DataHexString; amount: BigNumber };

export type Deposit = { trader: Address; strategy: string; currency: Address; amount: Address };

export type Withdraw = { trader: Address; strategy: string; currency: Address; amount: Address };

export enum OrderType {
    Limit = 'Limit',
    Market = 'Market',
    StopLimit = 'StopLimit',
}

export type OrderIntent = {
    traderAddress: Address;
    symbol: string;
    strategy: string;
    side: OrderSide;
    orderType: OrderType;
    nonce: DataHexString;
    amount: BigNumber;
    price: BigNumber;
    stopPrice: BigNumber;
    signature: RawSignature;
};

export type CancelOrderIntent = {
    orderHash: DataHexString;
    nonce: DataHexString;
    signature: RawSignature;
};

export type WithdrawIntent = {
    trader: Address;
    strategyId: string;
    currency: Address;
    amount: BigNumber;
    nonce: DataHexString;
    signature: RawSignature;
};

export enum OrderSide {
    Bid = 'Bid',
    Ask = 'Ask',
}
