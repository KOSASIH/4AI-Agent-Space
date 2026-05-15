const hre = require("hardhat");

async function main() {
  const [deployer] = await hre.ethers.getSigners();
  
  console.log("Deploying contracts with:", deployer.address);
  
  // Deploy token
  const Token = await hre.ethers.getContractFactory("AgentEconomyToken");
  const token = await Token.deploy();
  await token.waitForDeployment();
  
  // Deploy marketplace
  const Marketplace = await hre.ethers.getContractFactory("AgentMarketplace");
  const marketplace = await Marketplace.deploy(await token.getAddress());
  await marketplace.waitForDeployment();
  
  console.log("Token deployed to:", await token.getAddress());
  console.log("Marketplace deployed to:", await marketplace.getAddress());
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
