from datetime import datetime, timedelta

from otree.views.admin import AdminReport

from ._builtin import Page, WaitPage


class MyPage(Page):
    form_model = 'player'


class ResultsWaitPage(WaitPage):
    pass


class SessionBase(object):

    def post(self, *args, **kwargs):
        session_payoff = 4000
        percentage_saved = self.player.percentage_saved
        saved = 0
        if self.player.money_decision == 0:
            disbursement = 4000
        elif self.player.money_decision == 1:
            saved = (percentage_saved / 100) * session_payoff
            disbursement = session_payoff - saved
        else:
            saved = session_payoff
            disbursement = 0
        if saved:
            money = 50 if self.player.intermedio_actual == 1 else 25
            saved += int((saved / 100) * money)
        self.player.payoff = self.player.payoff + saved
        self.player.disbursement = self.player.disbursement + disbursement
        self.player.save()
        return super(SessionBase, self).post(*args, **kwargs)


class EncuestaSocioEconomica(Page):
    template_name = 'experimiento_1/encuesta_economica.html'
    form_model = 'player'
    form_fields = ['survey']


class Session1(SessionBase, Page):
    template_name = 'experimiento_1/session_1.html'
    form_model = 'player'
    form_fields = ['file_session_1']
    document = 'experimento_1/session_1.pdf'
    text_info = "Las siguientes páginas hacen parte del libro El crimen como oficio: ensayos sobre economía del crimen en Colombia (2007), y es necesario para nosotros transcribir la información contenida en el documento. El tiempo aproximado del siguiente trabajo es de 15 min, por favor transcriba la información en el espacio disponible. "

    def get_context_data(self, *args, **kwargs):
        context = super(Session1, self).get_context_data(*args, **kwargs)
        context['text_info'] = self.text_info
        context['document_url'] = self.document
        return context


class Session2(SessionBase, Page):
    template_name = 'experimiento_1/session_1.html'
    form_model = 'player'
    form_fields = ['file_session_2']
    document = 'experimento_1/session_2.pdf'

    text_info = "Las siguientes páginas hacen parte del libro Informe de la desigualdad global (2018), y es necesario para nosotros transcribir la información contenida en el documento. El tiempo aproximado del siguiente trabajo es de 15 min, por favor transcriba la información en el espacio disponible. "

    def get_context_data(self, *args, **kwargs):
        context = super(Session2, self).get_context_data(*args, **kwargs)
        context['text_info'] = self.text_info
        context['document_url'] = self.document
        return context


class Session3(SessionBase, Page):
    template_name = 'experimiento_1/session_1.html'
    form_model = 'player'
    form_fields = ['file_session_3']
    document = 'experimento_1/session_3.pdf'
    text_info = "Las siguientes páginas hacen parte del libro Informe de la desigualdad global (2018), y es necesario para nosotros transcribir la información contenida en el documento. El tiempo aproximado del siguiente trabajo es de 15 min, por favor transcriba la información en el espacio disponible. "

    def get_context_data(self, *args, **kwargs):
        context = super(Session3, self).get_context_data(*args, **kwargs)
        context['text_info'] = self.text_info
        context['document_url'] = self.document
        return context


class Session4(Page):
    template_name = 'experimiento_1/session_2.html'
    form_model = 'player'
    form_fields = ['monto_session_2']


class IntermedioSession(Page):
    template_name = 'experimiento_1/intermedio.html'
    form_model = 'player'
    form_fields = ['money_decision', 'percentage_saved']

    def get_context_data(self, *args, **kwargs):
        context = super(IntermedioSession, self).get_context_data(*args, **kwargs)
        return context

    def get_form(self, *args, **kwargs):
        form = super(IntermedioSession, self).get_form(*args, **kwargs)
        new_decisions = []
        money = 50 if self.player.intermedio_actual == 1 else 25
        for field in form.fields['money_decision'].choices:
            new_decisions.append((field[0], field[1].format(price_session=money)))
        form.fields['money_decision'].choices = new_decisions
        return form

    def post(self, *args, **kwargs):
        money_decision = self.request.POST.get('money_decision')
        percentage_saved = self.request.POST.get('percentage_saved')

        self.player.intermedio = self.player.intermedio + 1
        self.player.save()
        return super(IntermedioSession, self).post(*args, **kwargs)


class SevenDaysWaitPage(Page):
    template_name = 'experimiento_1/wait_page.html'

    def get_context_data(self, *args, **kwargs):
        day_available = self.player.updated_at.replace(hour=0, tzinfo=None) + timedelta(days=7)
        today = datetime.now()
        context = super(SevenDaysWaitPage, self).get_context_data(*args, **kwargs)
        context['day_available'] = day_available
        context['can_access'] = today > day_available
        return context


class Consent(Page):
    form_model = 'player'  # Le dice que es un jugador
    form_fields = ['num_temporal', 'accepts_terms']


page_sequence = [
    Consent,
    MyPage,
    IntermedioSession,
    Session1,
    IntermedioSession,
    # SevenDaysWaitPage,
    Session2,
    # SevenDaysWaitPage,
    Session3,
    EncuestaSocioEconomica,
    Session4,
]
