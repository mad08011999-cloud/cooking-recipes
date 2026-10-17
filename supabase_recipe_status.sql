-- Run once in the Supabase SQL editor (project mazrqepjgdtdraxpcptk) to enable account sync for the cookbook.
create table if not exists public.recipe_status(
  user_id uuid not null references auth.users(id) on delete cascade default auth.uid(),
  recipe_id text not null,
  saved boolean not null default false,
  cooked boolean not null default false,
  updated_at timestamptz not null default now(),
  primary key(user_id, recipe_id));
alter table public.recipe_status enable row level security;
create policy "own rows select" on public.recipe_status for select using (auth.uid() = user_id);
create policy "own rows insert" on public.recipe_status for insert with check (auth.uid() = user_id);
create policy "own rows update" on public.recipe_status for update using (auth.uid() = user_id) with check (auth.uid() = user_id);
create policy "own rows delete" on public.recipe_status for delete using (auth.uid() = user_id);
