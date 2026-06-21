# src/ui/consultancy_checker.py
import streamlit as st
from src.services.consultancy_service import predict_consultancy

def render_consultancy_checker_page():
    # Page hero
    st.markdown(
        """
<div class="hero-container">
    <div class="hero-title">Consultancies Checker</div>
    <div class="hero-subtitle">
        Check consultancy names and messages for potential fraud risk before you apply.
    </div>
</div>
""",
        unsafe_allow_html=True,
    )

    # Consultancy Legitimacy Checker
    st.markdown(
        """
<div class="section-header">
    <div class="section-icon">🏢</div>
    <div class="section-title">Consultancy Legitimacy Checker</div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        '<p style="color:#94a3b8; font-size:0.88rem; margin-bottom:1rem;">'
        "Provide details about the consultancy to estimate whether it looks <strong>Real</strong> or <strong>Fake</strong>. "
        "If you have trained the advanced model, it will use both the name and the message content plus whether they ask for fees."
        "</p>",
        unsafe_allow_html=True,
    )

    consultancy_name = st.text_input(
        "Consultancy / agency name",
        placeholder="e.g. Global Tech Solutions Pvt Ltd",
        key="consultancy_name_input",
    )

    consultancy_desc = st.text_area(
        "Message / description from consultancy (optional)",
        placeholder="Paste email, WhatsApp message, or about text from the consultancy here...",
        height=140,
        key="consultancy_desc_input",
    )

    asks_fee = st.checkbox(
        "This consultancy is asking for registration / joining / processing fees",
        key="consultancy_asks_fee",
    )

    if st.button("Check Consultancy"):
        name = consultancy_name.strip()

        if not name:
            st.error("Please enter a consultancy name to analyze.")
        else:
            result = predict_consultancy(
                name,
                description=consultancy_desc or "",
                asks_fee=asks_fee,
            )

            # Handle "name only but not found in database" case
            if "error" in result:
                st.warning(result["error"])
            else:
                label = result["label"]
                color = "#f97373" if label == "Fake Consultancy" else "#22c55e"

                # Unified confidence score (0–100) from either DB lookup or ML model
                confidence = result.get("confidence")

                # Backwards fallback if confidence is missing but per-class probs exist
                if confidence is None:
                    fake_prob = result.get("fake_probability")
                    real_prob = result.get("real_probability")
                    if label == "Fake Consultancy" and fake_prob is not None:
                        confidence = fake_prob
                    elif label == "Real Consultancy" and real_prob is not None:
                        confidence = real_prob

                if confidence is None:
                    confidence = 0.0

                st.markdown(
                    f"""
<div class="card-improve">
<h4>Consultancy Assessment</h4>

<p style="font-size:0.9rem; margin-bottom:0.5rem;">
This consultancy is assessed as:
<span style="font-weight:600; color:{color};">{label}</span>
&nbsp;(confidence: {confidence:.0f}%)
</p>

<p style="font-size:0.8rem; color:#94a3b8; margin-bottom:0.5rem;">
Source: {result.get("source","ML Model")}
</p>

</div>
""",
                    unsafe_allow_html=True,
                )

    st.markdown(
        """
<div style="text-align:center; padding:1rem 0 2rem 0;">
    <div style="font-size:0.82rem; color:#475569;">
        Built with Streamlit & Sentence-BERT • AI Career Compass Pro
    </div>
</div>
""",
        unsafe_allow_html=True,
    )
