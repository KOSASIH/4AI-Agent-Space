# Multi-cloud AI platform deployment
provider "aws" {
  region = "us-east-1"
}

module "eks_cluster" {
  source  = "terraform-aws-modules/eks/aws"
  cluster_name = "ai-agent-platform"
  cluster_version = "1.28"
  
  vpc_id = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets
  
  eks_managed_node_groups = {
    agents = {
      min_size     = 3
      max_size     = 50
      desired_size = 10
      instance_types = ["m6i.2xlarge"]
    }
  }
}

# GPU nodes for advanced models
resource "aws_eks_node_group" "gpu_agents" {
  cluster_name    = module.eks_cluster.cluster_id
  node_group_name = "gpu-agents"
  node_role_arn   = aws_iam_role.eks_node_role.arn
  
  instance_types = ["g5.2xlarge"]  # NVIDIA A10G GPUs
  scaling_config {
    desired_size = 2
    max_size     = 20
    min_size     = 1
  }
}
