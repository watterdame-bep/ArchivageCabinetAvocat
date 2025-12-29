<script>
						function printPaymentHistory() {
							const facture = document.getElementById('invoice-print-version');
							const iframe = document.getElementById('print-frame');
							const doc = iframe.contentDocument || iframe.contentWindow.document;

							doc.open();
							doc.write(`
<html>
<head>
    <title>Facture</title>
    <style>
        @page {
            size: A4;
            margin: 0;
        }
        body {
            margin: 0;
            padding: 0;
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
            position: relative;
			font-family: 'Roboto', sans-serif;
        }
        /* IMAGE DE FOND */
        body::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: url('/static/images/facture_bg.png') no-repeat center top;
            background-size: cover;
            z-index: -1;
        }

        /* CONTENU AVEC MARGE */
        .invoice-wrapper {
            padding: 20mm; /* ajustable */
            box-sizing: border-box;
        }

        .invoice-header {
            display:flex;
            justify-content:space-between;
            border-bottom:3px solid #2c3e50;
            padding-bottom:10px;
            margin-bottom:20px;
        }
        .invoice-header img { width:120px; height:auto; }
        .info-section { display:flex; justify-content:space-between; margin-bottom:25px; font-size:14px; }
        .info-section h3 { margin-bottom:8px; color:#2c3e50; }
        table { width:100%; border-collapse:collapse; font-size:13px; margin-bottom:20px; background: transparent; }
        table th, table td { border:1px solid #ddd; padding:8px; }
        table thead tr { background:#005582; color:white; }
        table tbody tr:nth-child(even) { background: rgba(0,0,0,0.05); }
        .totals { text-align:right; font-size:16px; margin-top:20px; }
        .invoice-footer { margin-top:40px; border-top:1px solid #ccc; padding-top:10px; font-size:12px; text-align:center; }
    </style>
</head>
<body>
    <div class="invoice-wrapper">
        ${facture.innerHTML}
    </div>
</body>
</html>
    `);
							doc.close();

							// Impression
							setTimeout(() => {
								iframe.contentWindow.focus();
								iframe.contentWindow.print();
							}, 500); // petit délai pour que le rendu soit complet
						}

					</script>