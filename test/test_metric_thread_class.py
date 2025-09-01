import json
import thread_fast


input_dict = {

}


M6_1_ext = thread_fast.MetricThread(
    name='M6x1.0',
    basic_major_diameter=6.0,
    pitch=1.0,
    tolerance_grade=4,
    allowance_class='h',
    external=True,
    profile='M',
    beta_rad=30.0 * thread_fast.cf.deg_to_rad,
)
print(M6_1_ext)
print(M6_1_ext.to_dict())

M6_1_ext2 = thread_fast.ExternalMetricThread(
    name='M6x1.0',
    basic_major_diameter=6.0,
    pitch=1.0,
    tolerance_grade=4,
    allowance_class='h',
    profile='M',
    beta_rad=30.0 * thread_fast.cf.deg_to_rad,
)
print(M6_1_ext2)
print(M6_1_ext2.to_dict())
M6_1_ext2.write_to_json('test_external_metric_thread.json')

M6_1_int = thread_fast.MetricThread(
    name='M6x1.0',
    basic_major_diameter=6.0,
    pitch=1.0,
    tolerance_grade=4,
    allowance_class='H',
    internal=True,
    profile='M',
    beta_rad=30.0 * thread_fast.cf.deg_to_rad,
)
print(M6_1_int)
print(M6_1_int.to_dict())

M6_1_int2 = thread_fast.InternalMetricThread(
    name='M6x1.0',
    basic_major_diameter=6.0,
    pitch=1.0,
    tolerance_grade=4,
    allowance_class='H',
    profile='M',
    beta_rad=30.0 * thread_fast.cf.deg_to_rad,
)
print(M6_1_int2)
print(M6_1_int2.to_dict())
M6_1_int2.write_to_json('test_internal_metric_thread.json')


