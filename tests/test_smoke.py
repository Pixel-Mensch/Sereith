from ai_pnp.core.application import Application

def test_application_boots():
    app = Application()
    assert app.engine.state.player.name
