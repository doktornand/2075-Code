#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Parseur des dimensions temporelles
"""

import re
from datetime import datetime

class TemporalParser:
    """Parseur des anomalies et éras temporelles"""
    
    def parse(self, text, config):
        """Analyse la dimension temporelle du texte"""
        eras_found = []
        time_signatures = []
        anomalies = []
        
        # Éras temporelles
        temporal_config = config.get('temporal', {})
        for era, data in temporal_config.items():
            indicators = data.get('indicators', [])
            era_indicators_found = []
            
            for indicator in indicators:
                if indicator.lower() in text.lower():
                    era_indicators_found.append(indicator)
            
            if era_indicators_found:
                eras_found.append({
                    'era': era,
                    'description': data.get('description', {}).get('fr', ''),
                    'aesthetic': data.get('aesthetic', []),
                    'indicators_found': era_indicators_found,
                    'confidence': len(era_indicators_found) / max(1, len(indicators))
                })
        
        # Signatures temporelles
        time_patterns = [
            (r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}Z', 'ISO-temporal-anomaly', 3),
            (r'\d{2}h\d{2}:\d{2}', 'tidal-time-signature', 2),
            (r'raz\s*•{3,}', 'void-temporal-suspension', 5),
            (r'\d{1,2}:\d{2}:\d{2}', 'chronometric-pulse', 1),
            (r'[OΩω]-*mega', 'omega-temporal-boundary', 10)
        ]
        
        for pattern, signature, weight in time_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                time_signatures.append({
                    'signature': signature,
                    'matches': matches,
                    'weight': weight,
                    'count': len(matches)
                })
                if weight >= 3:
                    anomalies.append(signature)
        
        # Calcul de cohérence temporelle
        temporal_coherence = self._calculate_temporal_coherence(eras_found, time_signatures)
        
        return {
            'eras': eras_found,
            'signatures': time_signatures,
            'anomalies': anomalies,
            'is_anachronic': len(eras_found) > 1,
            'temporal_coherence': temporal_coherence,
            'era_count': len(eras_found),
            'dominant_era': eras_found[0]['era'] if eras_found else 'present'
        }
    
    def _calculate_temporal_coherence(self, eras, signatures):
        """Calcule la cohérence temporelle"""
        base_coherence = 100
        
        # Pénalités pour anachronismes
        if len(eras) > 1:
            base_coherence -= (len(eras) - 1) * 20
        
        # Pénalités pour anomalies
        anomaly_penalty = sum(sig['weight'] * sig['count'] for sig in signatures if sig['weight'] >= 3)
        base_coherence -= anomaly_penalty
        
        return max(0, base_coherence)