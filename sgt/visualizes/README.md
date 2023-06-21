# Scatter Generate Tool Visuallizes

-----------

# subs_plot简介
> 实现基于子图的对照可视化绘图方法

## 1.主要内容
- 支持指定绘图画板大小
```python
subs_plot=SubgraphDrawing(
    graph_fig_size=[12, 9]
)
```
- 支持指定绘图子图排布——(原始图数量, 每个原始图对照数量+1)
```python
# origin_imgs: [., ., ...]
# map_imgs: [[...], [...], ...]
subs_plot=SubgraphDrawing(
    graph_shape=[len(origin_imgs), len(map_imgs[0])+1]
)
```
- 支持及时绘图显示
```python
subs_plot=SubgraphDrawing(
    graph_shape=[len(origin_imgs), len(map_imgs[0])+1],
    graph_fig_size=[12, 9]
)

subs_plot.plot(
    images=origin_imgs,
    labels=map_imgs,
    titles=None,
    save_path=None,
    plot_show=True # 绘图显示
)
```
- 支持绘图保存
```python
subs_plot=SubgraphDrawing(
    graph_shape=[len(origin_imgs), len(map_imgs[0])+1],
    graph_fig_size=[12, 9]
)

subs_plot.plot(
    images=origin_imgs,
    labels=map_imgs,
    titles=None,
    save_path='outputs/visual_imgs/subs_plot.png', # 绘图保存
    plot_show=False
)
```
- 支持自定义每组对照的title
```python
# len(origin_imgs) = 2
subs_plot=SubgraphDrawing(
    graph_shape=[len(origin_imgs), len(map_imgs[0])+1],
    graph_fig_size=[12, 9]
)
# 
subs_plot.plot(
    images=origin_imgs,
    labels=map_imgs,
    titles=['a', 'b'],
    save_path=None,
    plot_show=False
)
```

-----------

# match_plot简介
