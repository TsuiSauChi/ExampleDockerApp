'use strict';

const { Contract } = require('fabric-contract-api')

class TestContract extends Contract{

    async CreateAsset(ctx, id, amount) {
        const asset = {
            ID: id,
            Amount: amount
        };
        ctx.stub.putState(id, Buffer.from(JSON.stringify(asset)));
        return JSON.stringify(asset);
    }

    async ReadAsset(ctx, id) {
        const asset = await ctx.stub.getState(id);
        if (!asset || asset.length === 0){
            console.log('This asset does not exist')
            throw new Error('The asset does not exist')
        }
        return asset.toString();
    }
}

module.exports = TestContract