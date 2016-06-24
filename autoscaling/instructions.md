# RUN 

#### Single Instance Autoscaling

requires single_instance_scale.yaml ( call in [single_autoscale_env.yaml](https://github.com/savithruml/HOT-OpenStack/blob/master/autoscaling/single_autoscale_env.yaml) )

`# heat stack-create <stack-name> -f single_autoscale.yaml -e single_autoscale_env.yaml`

#### Contrail SI Scaling

requires contrail_si_scale.yaml ( call in [contrail_si_autoscale.yaml]())

`# heat stack-create <stack-name> -f contrail_si_autoscale.yaml -e contrail_si_autoscal.env`



