"""
CI/CD Pipeline Analytics - Light Theme Dashboard
Real-time data from Supabase
"""
import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from config import supabase

# Will be set when integrated with Flask
dash_app = None

# Light Theme
THEME = {
    'bg': '#f8fafc', 'card': '#ffffff', 'card_border': '#e2e8f0',
    'accent': '#6366f1', 'accent2': '#8b5cf6',
    'success': '#22c55e', 'error': '#ef4444', 'warning': '#f59e0b', 'info': '#3b82f6',
    'text': '#1e293b', 'text_dim': '#64748b', 'border': '#e2e8f0',
}

def fetch_jobs():
    result = supabase.table('jobs').select('*').order('created_at', desc=True).execute()
    if result.data:
        df = pd.DataFrame(result.data)
        df['created_at'] = pd.to_datetime(df['created_at'])
        df['started_at'] = pd.to_datetime(df['started_at'])
        df['finished_at'] = pd.to_datetime(df['finished_at'])
        df['date'] = df['created_at'].dt.date
        df['hour'] = df['created_at'].dt.hour
        df['day_name'] = df['created_at'].dt.day_name()
        df['duration'] = (df['finished_at'] - df['started_at']).dt.total_seconds()
        return df
    return pd.DataFrame()

def fetch_logs():
    result = supabase.table('job_logs').select('*').order('created_at', desc=True).limit(50).execute()
    return pd.DataFrame(result.data) if result.data else pd.DataFrame()

def fetch_users():
    result = supabase.table('users').select('*').execute()
    return pd.DataFrame(result.data) if result.data else pd.DataFrame()

def create_dashboard(flask_app):
    """Create and integrate Dash dashboard with Flask app"""
    global dash_app
    dash_app = dash.Dash(
        __name__, 
        server=flask_app, 
        url_base_pathname='/dashboard/',
        title="Pipeline Analytics"
    )
    
    dash_app.index_string = '''
<!DOCTYPE html>
<html>
<head>
    {%metas%}<title>{%title%}</title>{%favicon%}{%css%}
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Inter', -apple-system, sans-serif; background: #f8fafc; color: #1e293b; }
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: #f1f5f9; }
        ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
        .card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
        .card:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
        .pulse { animation: pulse 2s infinite; }
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
        .badge { padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: 500; }
    </style>
</head>
<body>{%app_entry%}<footer>{%config%}{%scripts%}{%renderer%}</footer></body>
</html>
'''

    dash_app.layout = html.Div([
    # Header
    html.Div([
        html.Div([
            html.H1("Pipeline Analytics", style={'fontSize': '20px', 'fontWeight': '600', 'color': THEME['text']}),
            html.Span("Real-time CI/CD Metrics", style={'color': THEME['text_dim'], 'fontSize': '13px', 'marginLeft': '16px'})
        ], style={'display': 'flex', 'alignItems': 'center'}),
        html.Div([
            html.A("← Back to App", href="/", style={
                'color': THEME['accent'], 'textDecoration': 'none', 'fontSize': '13px', 'marginRight': '20px', 'fontWeight': '500'
            }),
            html.Span("●", className='pulse', style={'color': THEME['success'], 'marginRight': '6px', 'fontSize': '10px'}),
            html.Span("Live", style={'fontSize': '13px', 'color': THEME['text_dim']})
        ], style={'display': 'flex', 'alignItems': 'center'})
    ], style={'display': 'flex', 'justifyContent': 'space-between', 'padding': '20px 32px', 
              'background': '#fff', 'borderBottom': f'1px solid {THEME["border"]}'}),
    
    # KPI Cards
    html.Div(id='kpi-cards', style={'display': 'grid', 'gridTemplateColumns': 'repeat(6, 1fr)', 'gap': '16px', 'padding': '24px 32px'}),
    
    # Row 1
    html.Div([
        html.Div([
            html.Div("Pipeline Throughput", style={'fontSize': '14px', 'fontWeight': '600', 'marginBottom': '16px', 'color': THEME['text']}),
            dcc.Graph(id='throughput-chart', config={'displayModeBar': False})
        ], className='card', style={'padding': '20px', 'flex': '2'}),
        html.Div([
            html.Div("Status Distribution", style={'fontSize': '14px', 'fontWeight': '600', 'marginBottom': '16px', 'color': THEME['text']}),
            dcc.Graph(id='status-pie', config={'displayModeBar': False})
        ], className='card', style={'padding': '20px', 'flex': '1'}),
    ], style={'display': 'flex', 'gap': '16px', 'padding': '0 32px 16px'}),
    
    # Row 2
    html.Div([
        html.Div([
            html.Div("Weekly Activity Heatmap", style={'fontSize': '14px', 'fontWeight': '600', 'marginBottom': '16px', 'color': THEME['text']}),
            dcc.Graph(id='heatmap-chart', config={'displayModeBar': False})
        ], className='card', style={'padding': '20px', 'flex': '1'}),
        html.Div([
            html.Div("Duration by Status", style={'fontSize': '14px', 'fontWeight': '600', 'marginBottom': '16px', 'color': THEME['text']}),
            dcc.Graph(id='duration-chart', config={'displayModeBar': False})
        ], className='card', style={'padding': '20px', 'flex': '1'}),
        html.Div([
            html.Div("Hourly Distribution", style={'fontSize': '14px', 'fontWeight': '600', 'marginBottom': '16px', 'color': THEME['text']}),
            dcc.Graph(id='hourly-chart', config={'displayModeBar': False})
        ], className='card', style={'padding': '20px', 'flex': '1'}),
    ], style={'display': 'flex', 'gap': '16px', 'padding': '0 32px 16px'}),
    
    # Row 3
    html.Div([
        html.Div([
            html.Div("Repository Performance", style={'fontSize': '14px', 'fontWeight': '600', 'marginBottom': '16px', 'color': THEME['text']}),
            dcc.Graph(id='repo-chart', config={'displayModeBar': False})
        ], className='card', style={'padding': '20px', 'flex': '1'}),
        html.Div([
            html.Div("Success vs Failure Trend", style={'fontSize': '14px', 'fontWeight': '600', 'marginBottom': '16px', 'color': THEME['text']}),
            dcc.Graph(id='trend-chart', config={'displayModeBar': False})
        ], className='card', style={'padding': '20px', 'flex': '1'}),
    ], style={'display': 'flex', 'gap': '16px', 'padding': '0 32px 16px'}),
    
    # Row 4
    html.Div([
        html.Div([
            html.Div("Recent Pipelines", style={'fontSize': '14px', 'fontWeight': '600', 'marginBottom': '16px', 'color': THEME['text']}),
            html.Div(id='jobs-table')
        ], className='card', style={'padding': '20px', 'flex': '2'}),
        html.Div([
            html.Div([
                html.Span("Live Logs", style={'fontSize': '14px', 'fontWeight': '600', 'color': THEME['text']}),
                html.Span("●", className='pulse', style={'color': THEME['success'], 'marginLeft': '8px', 'fontSize': '8px'})
            ], style={'marginBottom': '16px'}),
            html.Div(id='logs-feed', style={'height': '280px', 'overflowY': 'auto'})
        ], className='card', style={'padding': '20px', 'flex': '1'}),
    ], style={'display': 'flex', 'gap': '16px', 'padding': '0 32px 24px'}),
    
    dcc.Interval(id='refresh', interval=3000, n_intervals=0)
    ], style={'minHeight': '100vh', 'background': THEME['bg']})
    
    # Register callbacks
    register_callbacks(dash_app)
    
    return dash_app


def register_callbacks(app):
    @app.callback(
        [Output('kpi-cards', 'children'), Output('throughput-chart', 'figure'), Output('status-pie', 'figure'),
         Output('heatmap-chart', 'figure'), Output('duration-chart', 'figure'), Output('hourly-chart', 'figure'),
         Output('repo-chart', 'figure'), Output('trend-chart', 'figure'),
         Output('jobs-table', 'children'), Output('logs-feed', 'children')],
        [Input('refresh', 'n_intervals')]
    )
    def update_all(n):
        df = fetch_jobs()
        logs = fetch_logs()
        users = fetch_users()
        
        def empty_fig(h=200):
            fig = go.Figure()
            fig.add_annotation(text='No data available', x=0.5, y=0.5, xref='paper', yref='paper',
                              showarrow=False, font=dict(size=14, color=THEME['text_dim']))
            fig.update_layout(
                paper_bgcolor='#fff', plot_bgcolor='#fff', height=h, 
                margin=dict(l=20, r=20, t=20, b=20),
                xaxis=dict(visible=False, showgrid=False),
                yaxis=dict(visible=False, showgrid=False)
            )
            return fig
        
        if df.empty:
            kpis = [kpi_card("Total Jobs", 0, THEME['accent']), kpi_card("Success Rate", "0%", THEME['success']),
                    kpi_card("Failed", 0, THEME['error']), kpi_card("Running", 0, THEME['info']),
                    kpi_card("Avg Duration", "0s", THEME['warning']), kpi_card("Users", len(users), THEME['accent2'])]
            return kpis, empty_fig(220), empty_fig(220), empty_fig(200), empty_fig(200), empty_fig(200), empty_fig(200), empty_fig(200), \
                   html.P("No jobs yet - create a pipeline to see data here", style={'color': THEME['text_dim'], 'textAlign': 'center', 'padding': '40px'}), \
                   html.P("No logs yet", style={'color': THEME['text_dim'], 'textAlign': 'center', 'padding': '40px'})
        
        # Stats
        total = len(df)
        success = len(df[df['status'] == 'success'])
        failed = len(df[df['status'] == 'failed'])
        running = len(df[df['status'] == 'running'])
        rate = f"{success/total*100:.0f}%" if total else "0%"
        avg_dur = f"{df['duration'].dropna().mean():.0f}s" if df['duration'].notna().any() else "0s"
        
        kpis = [kpi_card("Total Jobs", total, THEME['accent']), kpi_card("Success Rate", rate, THEME['success']),
                kpi_card("Failed", failed, THEME['error']), kpi_card("Running", running, THEME['info']),
                kpi_card("Avg Duration", avg_dur, THEME['warning']), kpi_card("Users", len(users), THEME['accent2'])]
        
        # 1. Throughput Area
        daily = df.groupby('date').size().reset_index(name='count')
        throughput = go.Figure()
        throughput.add_trace(go.Scatter(x=daily['date'], y=daily['count'], mode='lines', fill='tozeroy',
                                        line=dict(color=THEME['accent'], width=2), fillcolor='rgba(99,102,241,0.1)'))
        throughput.update_layout(paper_bgcolor='#fff', plot_bgcolor='#fff', height=220, margin=dict(l=40,r=20,t=10,b=40),
                                xaxis=dict(showgrid=False, tickfont=dict(size=11, color=THEME['text_dim'])),
                                yaxis=dict(showgrid=True, gridcolor='#f1f5f9', tickfont=dict(size=11, color=THEME['text_dim'])))
        
        # 2. Status Pie
        status_counts = df['status'].value_counts()
        colors_map = {'success': THEME['success'], 'failed': THEME['error'], 'running': THEME['info'], 
                      'pending': THEME['text_dim'], 'cancelled': THEME['warning']}
        status_pie = go.Figure(go.Pie(values=status_counts.values, labels=status_counts.index, hole=0.5,
                                      marker=dict(colors=[colors_map.get(s, THEME['text_dim']) for s in status_counts.index]),
                                      textinfo='percent', textfont=dict(size=12, color='#fff')))
        status_pie.update_layout(paper_bgcolor='#fff', height=220, margin=dict(l=20,r=20,t=10,b=10),
                                legend=dict(orientation='h', y=-0.1, font=dict(size=11, color=THEME['text_dim'])))
        
        # 3. Heatmap
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        heatmap_data = df.groupby(['day_name', 'hour']).size().unstack(fill_value=0).reindex(days_order, fill_value=0)
        heatmap = go.Figure(go.Heatmap(z=heatmap_data.values, x=list(range(24)), y=['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],
                                       colorscale=[[0, '#f1f5f9'], [0.5, '#a5b4fc'], [1, THEME['accent']]], showscale=False))
        heatmap.update_layout(paper_bgcolor='#fff', plot_bgcolor='#fff', height=200, margin=dict(l=40,r=20,t=10,b=30),
                             xaxis=dict(tickfont=dict(size=10, color=THEME['text_dim']), dtick=4),
                             yaxis=dict(tickfont=dict(size=10, color=THEME['text_dim'])))
        
        # 4. Duration Box
        dur_df = df[df['duration'].notna()]
        if not dur_df.empty:
            duration = go.Figure()
            for status in ['success', 'failed']:
                subset = dur_df[dur_df['status'] == status]
                if not subset.empty:
                    duration.add_trace(go.Box(y=subset['duration'], name=status.title(), 
                                             marker_color=colors_map.get(status), boxpoints=False))
            duration.update_layout(paper_bgcolor='#fff', plot_bgcolor='#fff', height=200, margin=dict(l=50,r=20,t=10,b=30),
                                  showlegend=False, yaxis=dict(title=dict(text='Seconds', font=dict(size=11, color=THEME['text_dim'])), 
                                                              gridcolor='#f1f5f9',
                                                              tickfont=dict(size=10, color=THEME['text_dim'])))
        else:
            duration = empty_fig()
        
        # 5. Hourly Bar
        hourly = df.groupby('hour').size().reindex(range(24), fill_value=0)
        hourly_chart = go.Figure(go.Bar(x=list(range(24)), y=hourly.values, marker_color=THEME['accent']))
        hourly_chart.update_layout(paper_bgcolor='#fff', plot_bgcolor='#fff', height=200, margin=dict(l=40,r=20,t=10,b=30),
                                  xaxis=dict(tickfont=dict(size=10, color=THEME['text_dim']), dtick=4),
                                  yaxis=dict(showgrid=True, gridcolor='#f1f5f9', tickfont=dict(size=10, color=THEME['text_dim'])))
        
        # 6. Repo Bar
        repo_counts = df['repo_url'].value_counts().head(5)
        repo_names = [r.split('/')[-1][:15] if r else 'Unknown' for r in repo_counts.index]
        repo_chart = go.Figure(go.Bar(y=repo_names, x=repo_counts.values, orientation='h', marker_color=THEME['accent']))
        repo_chart.update_layout(paper_bgcolor='#fff', plot_bgcolor='#fff', height=200, margin=dict(l=100,r=20,t=10,b=30),
                                xaxis=dict(showgrid=True, gridcolor='#f1f5f9', tickfont=dict(size=10, color=THEME['text_dim'])),
                                yaxis=dict(tickfont=dict(size=11, color=THEME['text'])))
        
        # 7. Trend Line
        daily_stats = df.groupby('date').agg(success=('status', lambda x: (x=='success').sum()),
                                              failed=('status', lambda x: (x=='failed').sum())).reset_index()
        trend = go.Figure()
        trend.add_trace(go.Scatter(x=daily_stats['date'], y=daily_stats['success'], name='Success', mode='lines+markers',
                                   line=dict(color=THEME['success'], width=2), marker=dict(size=6)))
        trend.add_trace(go.Scatter(x=daily_stats['date'], y=daily_stats['failed'], name='Failed', mode='lines+markers',
                                   line=dict(color=THEME['error'], width=2), marker=dict(size=6)))
        trend.update_layout(paper_bgcolor='#fff', plot_bgcolor='#fff', height=200, margin=dict(l=40,r=20,t=10,b=40),
                           legend=dict(orientation='h', y=1.1, font=dict(size=11, color=THEME['text_dim'])),
                           xaxis=dict(showgrid=False, tickfont=dict(size=10, color=THEME['text_dim'])),
                           yaxis=dict(showgrid=True, gridcolor='#f1f5f9', tickfont=dict(size=10, color=THEME['text_dim'])))
        
        # Jobs Table
        table = create_table(df.head(8))
        
        # Logs Feed
        if not logs.empty:
            log_colors = {'info': THEME['info'], 'error': THEME['error'], 'warn': THEME['warning']}
            logs_feed = [html.Div([
                html.Span("●", style={'color': log_colors.get(row['level'], THEME['text_dim']), 'marginRight': '8px', 'fontSize': '8px'}),
                html.Span(str(row['message'])[:50], style={'fontSize': '12px', 'color': THEME['text']})
            ], style={'padding': '8px 0', 'borderBottom': f'1px solid {THEME["border"]}'}) for _, row in logs.head(20).iterrows()]
        else:
            logs_feed = [html.P("Waiting for logs...", style={'color': THEME['text_dim'], 'textAlign': 'center', 'padding': '40px'})]
        
        return kpis, throughput, status_pie, heatmap, duration, hourly_chart, repo_chart, trend, table, logs_feed


def kpi_card(label, value, color):
    return html.Div([
        html.Div(str(value), style={'fontSize': '28px', 'fontWeight': '700', 'color': color}),
        html.Div(label, style={'fontSize': '12px', 'color': THEME['text_dim'], 'marginTop': '4px'})
    ], className='card', style={'padding': '20px', 'textAlign': 'center'})


def create_table(df):
    if df.empty:
        return html.P("No jobs", style={'color': THEME['text_dim'], 'textAlign': 'center', 'padding': '40px'})
    colors = {'success': THEME['success'], 'failed': THEME['error'], 'running': THEME['info'], 
              'pending': THEME['text_dim'], 'cancelled': THEME['warning']}
    return html.Div([
        html.Div([
            html.Span("●", style={'color': colors.get(r['status'], THEME['text_dim']), 'marginRight': '12px', 'fontSize': '10px'}),
            html.Span(r['repo_url'].split('/')[-1] if r['repo_url'] else '-', style={'flex': '1', 'fontWeight': '500', 'fontSize': '13px'}),
            html.Span(r['branch'], style={'width': '100px', 'fontSize': '12px', 'color': THEME['text_dim']}),
            html.Span(r['status'], className='badge', style={
                'backgroundColor': f"{colors.get(r['status'], THEME['text_dim'])}15",
                'color': colors.get(r['status'], THEME['text_dim']), 'width': '80px', 'textAlign': 'center'
            }),
            html.Span(r['created_at'].strftime('%H:%M') if pd.notna(r['created_at']) else '', 
                     style={'width': '60px', 'fontSize': '12px', 'color': THEME['text_dim'], 'textAlign': 'right'})
        ], style={'display': 'flex', 'alignItems': 'center', 'padding': '12px 0', 'borderBottom': f'1px solid {THEME["border"]}'})
        for _, r in df.iterrows()
    ])


if __name__ == '__main__':
    # Standalone mode for testing
    from flask import Flask
    test_app = Flask(__name__)
    create_dashboard(test_app)
    print("\n  📊 Pipeline Analytics (Light Theme)")
    print(f"  → http://localhost:8050/dashboard/\n")
    test_app.run(debug=True, port=8050)
