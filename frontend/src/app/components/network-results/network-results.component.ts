import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';

interface NetworkTypeCoverage {
    [networkType: string]: boolean;
  }

  interface OperatorCoverage {
    [operatorName: string]: NetworkTypeCoverage;
  }

  interface NetworkResults {
    [addressId: string]: OperatorCoverage;
  }

@Component({
  selector: 'app-network-results',
  imports: [CommonModule, MatCardModule],
  templateUrl: './network-results.component.html',
  styleUrl: './network-results.component.css'
})
export class NetworkResultsComponent {
  @Input() results: NetworkResults | null = null;

  get operators(): string[] {
    if (!this.results) return [];
    const firstAddress = Object.values(this.results)[0];
    return Object.keys(firstAddress || {});
  }

  get addresses(): string[] {
    return Object.keys(this.results || {});
  }

  get networkTypes(): string[] {
    if (!this.results) return [];
    const firstAddress = Object.values(this.results)[0];
    if (!firstAddress) return [];
    const firstOperator = Object.values(firstAddress)[0];
    return Object.keys(firstOperator || {});
  }

  getStatusText(status: boolean): string {
    return status ? 'OK' : 'KO';
  }

  getCoverage(addressId: string, operator: string, networkType: string): boolean {
    return this.results?.[addressId]?.[operator]?.[networkType] || false;
  }
}
