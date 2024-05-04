import { Routes } from '@angular/router';
import { AuthGuard } from './service/auth.guard';
import { LoginComponent } from './pages/login/login.component';
import { SignupComponent } from './pages/signup/signup.component';
import { DashboardComponent } from './pages/dashboard/dashboard.component';
import { TransactionComponent } from './pages/transaction/transaction.component';
import { HistoryComponent } from './pages/history/history.component';
import { CardmanagementComponent } from './pages/cardmanagement/cardmanagement.component';

export const routes: Routes = [
    {
        path: '', redirectTo: 'login', pathMatch :'full'
    },
    {
        path: 'login',
        component:LoginComponent
    },
    { 
        path: 'dashboard', component: DashboardComponent, canActivate: [AuthGuard]
    },
    {
        path: 'transaction', component: TransactionComponent
    },
    {
        path: 'history', component: HistoryComponent
    },
    {
        path: 'cardmanagement', component: CardmanagementComponent
    },
    {
        path: 'signup',
        component:SignupComponent
    },
];