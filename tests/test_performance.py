#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By   : Charley ∆. Lebarbier
# Date Created : Wednesday 1 Mai 2024
# ==============================================================================

import utils.functions as fct

class TestLoadModelPerformance:

    def test_load_model_performance(self, benchmark):
        def load_model():
            return fct.load_model()

        result = benchmark(load_model)

        assert result is not None
