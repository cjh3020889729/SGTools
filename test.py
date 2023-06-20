from sgt.env.logger import create_logger
from sgt.transforms import transforms, batch_transforms
from sgt.visualizes.subs_plot import SubgraphDrawing
from sgt.env.register import register

logger = create_logger(log_name=__name__)
logger.info("Test Module is Loaded!")

# subs_plot=SubgraphDrawing(
#     graph_shape=[1, 1],
#     graph_fig_size=[12, 9]
# )

subs_plot=register.get('SubgraphDrawing')(
    graph_shape=[1, 1],
    graph_fig_size=[12, 9]
)
