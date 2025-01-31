resource "aws_rds_cluster" "aurora" {
  cluster_identifier     = "serverless-cluster"
  engine                 = "aurora-mysql"
  engine_version         = "8.0.mysql_aurora.3.06.1"
  engine_mode            = "provisioned"
  database_name          = "mydatabase"
  master_username        = "admin"
  master_password        = "admin123"
  storage_encrypted  = true

  serverlessv2_scaling_configuration {
    min_capacity = 2
    max_capacity = 3
  }
}

resource "aws_rds_cluster_instance" "serverless" {
  cluster_identifier = aws_rds_cluster.aurora.id
  instance_class     = "db.serverless"
  engine             = aws_rds_cluster.aurora.engine
  engine_version     = aws_rds_cluster.aurora.engine_version
}