import flot
import datetime
from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        xy10 = flot.Series(x=flot.XVariable(points=range(1, 10)),
                           y=flot.YVariable(points=range(1, 10))) 

        xy20 = flot.Series(x=flot.XVariable(points=[i for i in range(1, 10)]),
                           y=flot.YVariable(points=[i*2 for i in range(1, 10)]))

        x_time_points = [datetime.date(2011, 1, i) for i in range(1, 20)]
        y_points = [float(1)/i for i in range(1, 20)]
        time1 = flot.Series(x=flot.TimeXVariable(points=x_time_points),
                            y=flot.YVariable(points=y_points))

        context = {
                    'graph1': flot.Graph(series1=xy10, series2=xy20),
                    'graph2': flot.Graph(series1=time1),
                }
        return context
