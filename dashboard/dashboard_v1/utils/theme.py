# Modern Blue Theme Colors
BG_COLOR = "#0B1426"
CARD_COLOR = "#131F37"
COLOR_PRIMARY = "#3B82F6"
COLOR_SECONDARY = "#F43F5E"
COLOR_GREEN = "#10B981"
TEXT_COLOR = "#F8FAFC"

def style_chart(fig):
    """Applies the global theme to Plotly figures."""
    fig.update_layout(
        plot_bgcolor=BG_COLOR,
        paper_bgcolor=BG_COLOR,
        font=dict(color=TEXT_COLOR),
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig