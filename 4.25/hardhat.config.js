require("@nomicfoundation/hardhat-toolbox");
require("hardhat-output-validator");

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity: {
    version: "0.4.24",
    settings: {
      	optimizer: {
        	enabled: true,
        	runs: 1000
      	},
        "viaIR":true
    }
   },
};
