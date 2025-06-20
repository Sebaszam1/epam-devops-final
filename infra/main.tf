module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.1.2"

  name = "${var.project_name}-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["us-east-1a", "us-east-1b"]
  public_subnets  = ["10.0.1.0/24", "10.0.2.0/24"]
  private_subnets = ["10.0.3.0/24", "10.0.4.0/24"]

  enable_nat_gateway   = true
  single_nat_gateway   = true
  enable_dns_hostnames = true

  //Used to identify the public subnets for the EKS cluster
  public_subnet_tags = {
    "kubernetes.io/role/elb"                        = "1"
    "kubernetes.io/cluster/${var.project_name}-eks" = "owned"
  }

  //Used to identify the private subnets for the EKS cluster
  private_subnet_tags = {
    "kubernetes.io/role/internal-elb"               = "1"
    "kubernetes.io/cluster/${var.project_name}-eks" = "owned"
  }
}

module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  version         = "20.8.4"
  cluster_name    = "${var.project_name}-eks"
  cluster_version = "1.29"
  subnet_ids      = module.vpc.private_subnets
  vpc_id          = module.vpc.vpc_id

  # Enable public endpoint for CI/CD access (GitHub actions)
  cluster_endpoint_public_access  = true
  cluster_endpoint_private_access = true

  # Enable cluster creator admin permissions (GitHub actions)
  enable_cluster_creator_admin_permissions = true

  eks_managed_node_groups = {
    default = {
      instance_types = ["t3.small"]
      min_size       = 1
      max_size       = 2
      desired_size   = 1
    }
  }
}

# AWS Load Balancer Controller IAM Role

#Create document to trust the AWS Load Balancer Controller IAM role
data "aws_iam_policy_document" "aws_load_balancer_controller_trust_policy" {
  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]
    effect  = "Allow"

    #Verify the OIDC provider is the same as the one in the EKS cluster 
    condition {
      test     = "StringEquals"
      variable = "${replace(module.eks.cluster_oidc_issuer_url, "https://", "")}:sub"
      values   = ["system:serviceaccount:kube-system:aws-load-balancer-controller"]
    }

    #Verify the OIDC was created in the EKS cluster
    principals {
      identifiers = [module.eks.oidc_provider_arn]
      type        = "Federated"
    }
  }
}

#Create the IAM role for the AWS Load Balancer Controller
resource "aws_iam_role" "aws_load_balancer_controller" {
  assume_role_policy = data.aws_iam_policy_document.aws_load_balancer_controller_trust_policy.json
  name               = "${var.project_name}-aws-load-balancer-controller"
}

#Create the IAM policy for the AWS Load Balancer Controller
resource "aws_iam_policy" "aws_load_balancer_controller" {
  policy = file("${path.module}/iam-policy.json")
  name   = "${var.project_name}-AWSLoadBalancerControllerIAMPolicy"
}

#Attach the IAM policy to the IAM role
resource "aws_iam_role_policy_attachment" "aws_load_balancer_controller" {
  policy_arn = aws_iam_policy.aws_load_balancer_controller.arn
  role       = aws_iam_role.aws_load_balancer_controller.name
}
