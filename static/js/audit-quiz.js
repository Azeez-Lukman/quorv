// Beauty Digital Audit Engine & Modal Controller
document.addEventListener('DOMContentLoaded', () => {
  const modal = document.getElementById('auditModal');
  const openButtons = document.querySelectorAll('.open-audit-modal');
  const closeBtn = document.getElementById('closeAuditModal');
  const form = document.getElementById('auditForm');
  const step1 = document.getElementById('auditStep1');
  const step2 = document.getElementById('auditStep2');
  const step3 = document.getElementById('auditStep3');
  const nextBtn = document.getElementById('auditNextBtn');
  const submitBtn = document.getElementById('auditSubmitBtn');
  const resultsContainer = document.getElementById('auditResultsContainer');

  let currentStep = 1;

  function openAudit() {
    if (!modal) return;
    modal.classList.remove('hidden');
    modal.classList.add('flex');
    document.body.style.overflow = 'hidden';
    setStep(1);
  }

  function closeAudit() {
    if (!modal) return;
    modal.classList.add('hidden');
    modal.classList.remove('flex');
    document.body.style.overflow = '';
  }

  openButtons.forEach(btn => btn.addEventListener('click', (e) => {
    e.preventDefault();
    openAudit();
  }));

  if (closeBtn) closeBtn.addEventListener('click', closeAudit);
  if (modal) {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) closeAudit();
    });
  }

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal && !modal.classList.contains('hidden')) {
      closeAudit();
    }
  });

  function setStep(step) {
    currentStep = step;
    if (step1) step1.classList.toggle('hidden', step !== 1);
    if (step2) step2.classList.toggle('hidden', step !== 2);
    if (step3) step3.classList.toggle('hidden', step !== 3);
    if (resultsContainer) resultsContainer.classList.add('hidden');

    const progressPills = document.querySelectorAll('.audit-step-pill');
    progressPills.forEach((pill, idx) => {
      if (idx + 1 === step) {
        pill.classList.add('bg-[#E4C388]', 'text-[#08090C]', 'font-bold');
        pill.classList.remove('bg-white/10', 'text-white/60');
      } else if (idx + 1 < step) {
        pill.classList.add('bg-[#E4C388]/30', 'text-[#E4C388]');
        pill.classList.remove('bg-white/10', 'text-white/60', 'bg-[#E4C388]', 'text-[#08090C]');
      } else {
        pill.classList.add('bg-white/10', 'text-white/60');
        pill.classList.remove('bg-[#E4C388]', 'text-[#08090C]', 'bg-[#E4C388]/30', 'text-[#E4C388]', 'font-bold');
      }
    });
  }

  if (nextBtn) {
    nextBtn.addEventListener('click', () => {
      if (currentStep === 1) {
        const bName = document.getElementById('auditBusinessName')?.value.trim();
        if (!bName) {
          alert('Please enter your business or studio name.');
          return;
        }
        setStep(2);
      } else if (currentStep === 2) {
        setStep(3);
      }
    });
  }

  const prevButtons = document.querySelectorAll('.audit-prev-btn');
  prevButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      if (currentStep > 1) setStep(currentStep - 1);
    });
  });

  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span>Analyzing Digital Architecture...</span>';
      }

      const payload = {
        business_name: document.getElementById('auditBusinessName')?.value || '',
        business_type: document.querySelector('input[name="audit_sector"]:checked')?.value || 'Salon',
        website_or_instagram: document.getElementById('auditWebsite')?.value || '',
        booking_software: document.querySelector('input[name="audit_booking"]:checked')?.value || 'Fresha',
        primary_challenge: document.querySelector('input[name="audit_challenge"]:checked')?.value || 'Low booking conversion',
        contact_name: document.getElementById('auditContactName')?.value || '',
        email: document.getElementById('auditEmail')?.value || '',
        phone: document.getElementById('auditPhone')?.value || '',
      };

      try {
        const res = await fetch('/api/audit/submit/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') || ''
          },
          body: JSON.stringify(payload)
        });

        const data = await res.json();
        if (data.status === 'success') {
          displayAuditResults(data.score, data.vulnerabilities, payload.business_name, data.dm_url, data.wa_url, data.dm_message);
        } else {
          alert(data.message || 'Something went wrong. Please reach out via Instagram.');
          if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<span>Calculate Health Score →</span>';
          }
        }
      } catch (err) {
        alert('Network error. Please contact Quorv on Instagram.');
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.innerHTML = '<span>Calculate Health Score →</span>';
        }
      }
    });
  }

  function displayAuditResults(score, vulnerabilities, businessName, dmUrl, waUrl, dmMessage) {
    if (step1) step1.classList.add('hidden');
    if (step2) step2.classList.add('hidden');
    if (step3) step3.classList.add('hidden');
    if (resultsContainer) {
      resultsContainer.classList.remove('hidden');

      const scoreNum = document.getElementById('auditScoreNumber');
      const scoreRating = document.getElementById('auditScoreRating');
      const scoreDesc = document.getElementById('auditScoreDesc');
      const vulnList = document.getElementById('auditVulnList');
      const messagePreview = document.getElementById('auditMessagePreview');
      const copyBtn = document.getElementById('copyAuditTextBtn');
      const copyBtnText = document.getElementById('copyBtnText');
      const openDmBtn = document.getElementById('openAuditDmBtn');
      const waBtn = document.getElementById('auditWaBtn');
      const toast = document.getElementById('auditClipboardToast');
      const toastMessage = document.getElementById('toastMessage');

      if (scoreNum) scoreNum.textContent = score;

      let ratingText = "Needs System Upgrade";
      let ratingColor = "text-amber-400";
      if (score < 55) {
        ratingText = "High Booking & Brand Leakage";
        ratingColor = "text-red-400";
      } else if (score >= 75) {
        ratingText = "Moderate Digital Health";
        ratingColor = "text-emerald-400";
      }

      if (scoreRating) {
        scoreRating.textContent = ratingText;
        scoreRating.className = `font-mono text-xs uppercase tracking-widest ${ratingColor} font-semibold`;
      }

      if (scoreDesc) {
        scoreDesc.textContent = `Diagnostic review for ${businessName}. Based on industry benchmarks across Mayfair, Manhattan, and Dubai clinics:`;
      }

      if (vulnList && vulnerabilities) {
        vulnList.innerHTML = vulnerabilities.map(v => `
          <li class="flex items-start gap-2.5 text-xs font-mono audit-vuln-item">
            <span class="text-[#E4C388] font-bold mt-0.5 flex-shrink-0">⚠️</span>
            <span class="vuln-text leading-relaxed font-medium">${v}</span>
          </li>
        `).join('');
      }

      const formattedMessage = dmMessage || `Hi Quorv, I just completed a digital audit on quorv.org for ${businessName}.

Health Score: ${score}/100

Friction points noted:
${(vulnerabilities || []).map(v => `• ${v}`).join('\n')}

I'd like to discuss fixing these issues and upgrading our digital systems.`;

      if (messagePreview) {
        messagePreview.textContent = formattedMessage;
      }

      const instagramDmTarget = dmUrl || 'https://ig.me/m/quorv_01';

      // Pre-copy results to clipboard so it's instantly ready
      copyToClipboard(formattedMessage);

      function showToast(msg) {
        if (!toast) return;
        if (toastMessage) toastMessage.textContent = msg;
        toast.classList.remove('hidden');
        setTimeout(() => {
          toast.classList.add('hidden');
        }, 3500);
      }

      function copyToClipboard(text, cb) {
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(text).then(() => {
            if (cb) cb();
          }).catch(() => {
            fallbackCopy(text, cb);
          });
        } else {
          fallbackCopy(text, cb);
        }
      }

      function fallbackCopy(text, cb) {
        const ta = document.createElement('textarea');
        ta.value = text;
        ta.style.position = 'fixed';
        ta.style.top = '-9999px';
        document.body.appendChild(ta);
        ta.focus();
        ta.select();
        try {
          document.execCommand('copy');
          if (cb) cb();
        } catch (e) {
          console.warn('Copy error:', e);
        }
        document.body.removeChild(ta);
      }

      if (copyBtn) {
        copyBtn.onclick = (e) => {
          e.preventDefault();
          copyToClipboard(formattedMessage, () => {
            if (copyBtnText) copyBtnText.textContent = '✓ Copied!';
            showToast('✓ Summary copied to clipboard!');
            setTimeout(() => {
              if (copyBtnText) copyBtnText.textContent = 'Copy Summary';
            }, 2500);
          });
        };
      }

      if (openDmBtn) {
        openDmBtn.href = instagramDmTarget;
        openDmBtn.onclick = function() {
          copyToClipboard(formattedMessage);
          showToast('✓ Summary copied! Opening @quorv_01 in Instagram...');
          return true; // Allows native anchor target="_blank" to open immediately without popup blockers
        };
      }
    }
  }

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
});
