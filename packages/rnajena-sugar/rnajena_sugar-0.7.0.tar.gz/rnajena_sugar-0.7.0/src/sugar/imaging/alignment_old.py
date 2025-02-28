# (C) 2024, Tom Eulenfeld, MIT license
from warnings import warn
import matplotlib.pyplot as plt

import numpy as np

from sugar.data import gcode
from sugar.imaging.colors import get_color_scheme
from matplotlib.colors import to_rgb

def _get_colordict(color, alphabet, default='white', gap='-', gap_color='white'):
    if color is None:
        color = {l: 'C{}'.format(i % 10) for i, l in enumerate(alphabet)}
    try:
        color = to_rgb(color)
    except ValueError:
        if isinstance(color, dict):
            colord = color
        elif isinstance(color, (tuple, list)):
            colord = {l: color[i % len(color)]  for i, l in enumerate(alphabet)}
        else:
            colord = get_color_scheme(color)
    else:
        colord = {l: color for l in alphabet}
    for g in gap:
        colord.setdefault(g, gap_color)
    return {l: to_rgb(colord.get(l, default)) for l in list(alphabet) + list(gap)}


def plot_alignment(
        seqs, fname=None, *,
        gap='-',
        color='gray', gap_color='white',
        fts=None,
        fts_account_for_gaps=True,
        fts_type='color',
        fts_color=None,
        fts_color_by='type',
        fts_color_alpha=None,
        despine=True, despine_offset=None,
        xticks=True,
        ax=None, figsize=None,
        savefig_kw={},
        symbols=False,
        symbol_color='black',
        symbol_gap_color='black',
        symbol_kw=None,
        extent=None,
        #extentx=None,
        #extenty=None,
        aspect='auto',
        **kw
        ):
    """
    Plot an alignment



    aspect, extent, rasterize
    """
    if gap is None:
        gap = ''
    alphabet = sorted(set(''.join(str(seq) for seq in seqs)) - set(gap))
    color = _get_colordict(color, alphabet, gap=gap, gap_color=gap_color)
    if fts:
        if fts is True:
            fts = seqs.fts
        if isinstance(fts_color_by, str):
            metaget = fts_color_by
            fts_color_by = lambda ft: ft.meta.get(metaget)
        if fts_color is None:
            fts_color = ['C{}'.format(i) for i in range(10)]
        if isinstance(fts_color, str):
            fts_color = [fts_color]
        if not isinstance(fts_color, dict):
            d = {}
            i = 0
            for ft in fts:
                k = fts_color_by(ft)
                if k not in d:
                    d[k] = fts_color[i]
                    i = (i + 1) % len(fts_color)
            fts_color = d
        fts_color = {k: to_rgb(c) for k, c in fts_color.items()}

    lens = [len(seq) for seq in seqs]
    n = max(lens)
    if len(set(lens)) > 1:
        warn('fill up short sequences with empty space')
        seqs = seqs.copy().str.rjust(n)

    data = [[color[l] for l in seq.data] for seq in seqs]
    if fts:
        ftsd = fts.groupby('seqid')
        if fts_color_alpha is not None:
            data_fts = [[(1, 1, 1, 0) for l in seq.data] for seq in seqs]
        for i, seq in enumerate(seqs):
            for ft in ftsd.get(seq.id, []):
                slice = seq.slindex(gap=gap if fts_account_for_gaps else None)[ft]
                start, stop, _ = slice.indices(len(data[i]))
                if fts_color_alpha is None:
                    data[i][slice] = [fts_color[fts_color_by(ft)]] * (stop - start)
                else:
                    data_fts[i][slice] = [fts_color[fts_color_by(ft)] + (fts_color_alpha,)] * (stop - start)

    if ax is None:
        fig = plt.figure(figsize=figsize)
        ax = fig.add_axes([0, 0, 1, 1])
    else:
        fig = ax.get_figure()
    kw.setdefault('interpolation', 'none')
    kw.setdefault('origin', 'upper')
    kw.setdefault('aspect', 'auto')
    if extent is None:
        extent = [-0.5, n - 0.5, len(data) - 0.5, -0.5]
    ax.imshow(np.array(data), extent=extent, **kw)
    if fts and fts_color_alpha is not None:
        ax.imshow(np.array(data_fts), extent=extent, **kw)
    if symbols:
        if symbol_kw is None:
            symbol_kw = {}
        symbol_color = _get_colordict(symbol_color, alphabet, default='black', gap=gap, gap_color=symbol_gap_color)
        symbol_kw.setdefault('family', 'monospace')
        symbol_kw.setdefault('va', 'center_baseline')
        symbol_kw.setdefault('ha', 'center')
        bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        symbol_kw.setdefault('size', bbox.width * fig.dpi / n)
        dx = (extent[1] - extent[0]) / n
        dy = (extent[3] - extent[2]) / len(data)
        for i in range(len(data)):
            for j in range(n):
                xy = (extent[0] + dx * (0.5 + j), extent[3] - dy * (0.5 + i))
                l = seqs[i].data[j]
                ax.annotate(l, xy, color=symbol_color[l], **symbol_kw)
    if despine not in (False, None):
        if despine is True:
            despine=(True, True, True, True)
        import seaborn as sns
        sns.despine(None, ax, *despine, despine_offset)
    ax.set_yticks([])
    if xticks is not True:
        if xticks is False:
            xticks = []
        ax.set_xticks(xticks)
    if fname is not None:
        fig.savefig(fname, **savefig_kw)
        plt.close(fig)
    else:
        return ax

from sugar import read

seqs = read().sl(update_fts=True)[:, :100]
seqs[1][:10] = '-' * 10
print(seqs)
seqs.fts = seqs.fts.slice(10, 15)[:1]
print(seqs.fts)
plot_alignment(seqs, fname='test.pdf', fts=True, aspect=2, rasterized=True, color='0.8', symbols=True, symbol_color='flower', origin='upper')




