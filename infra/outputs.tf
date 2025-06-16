output "eks_cluster_name" {
  value = module.eks.cluster_name
}

output "alb_dns_name" {
  value = module.alb.lb_dns_name
}
